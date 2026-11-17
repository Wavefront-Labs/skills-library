---
id: computing-software.cloud-infrastructure-engineering.aws.rds-subnet-groups-and-connectivity-troubleshooting
name: rds-subnet-groups-and-connectivity-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, db-subnet-group, rds-connectivity, security-groups, publicly-accessible, connection-timeout-rds]
level: practitioner
status: docs-checked
description: "Design DB subnet groups and fix 'cannot connect to RDS': DNS, security groups, subnet routing, public accessibility, TLS, max connections and auth errors, step by step."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Troubleshooting.html#CHAP_Troubleshooting.Connecting", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS subnet groups and connectivity

## 1. DB subnet groups
A DB subnet group lists subnets where RDS may place the instance and standbys/replicas. The VPC needs at least two
subnets in two different Availability Zones (a Local Zone DB subnet group can have only one subnet).
```bash
aws rds create-db-subnet-group --db-subnet-group-name prod-db \
  --db-subnet-group-description "isolated data subnets" \
  --subnet-ids subnet-iso-a subnet-iso-b subnet-iso-c
```
- For a publicly accessible instance every subnet in the group must be public (internet gateway route); use
  subnets without an internet route for private databases.
- Define subnets in two or more AZs, even for Single-AZ instances, so you can convert to Multi-AZ later.
- Reserve at least one free IP address in each subnet of the group for RDS recovery actions.
- `modify-db-instance --db-subnet-group-name` is the parameter that moves an instance to a different subnet group
  or VPC; read the ModifyDBInstance documentation for the conditions before using it on production.
- Dual-stack needs an IPv6 CIDR on every subnet in the group.

## 2. Connection troubleshooting order
1. **Endpoint and port**: use the endpoint DNS name (never the IP; it changes on failover).
   `aws rds describe-db-instances --db-instance-identifier orders --query
   'DBInstances[].Endpoint'`.
2. **DNS resolution** from the client: `dig orders.xxxx.eu-west-1.rds.amazonaws.com`;
   private IP expected for private instances.
3. **Network path**: `nc -vz <endpoint> 5432` (or 3306, 1433, 1521).
   - Timeout: security group or NACL or routing.
   - Connection refused: wrong port, or instance not available (rebooting, storage-full).
4. **Security group** on the DB allows the port from the client's IP range or another security group. Connections
   from 169.254.0.0/16 (link-local) are not permitted.
5. **Routing**: client subnet route table reaches the DB VPC (peering/TGW routes, VPN
   propagation); on-prem firewalls allow the port.
6. **Public access** (only if truly needed): the instance needs a public IP address (publicly accessible = Yes),
   its subnets need an internet gateway, and the security group must allow the client's address. For access from
   outside the VPC all three matter.
7. **Reachability Analyzer** from client ENI to the RDS ENI on the DB port names the blocker.

## 3. Errors after the TCP connection works
| Error | Cause |
|---|---|
| `password authentication failed` / `Access denied for user` | wrong credentials; Secrets Manager rotation changed them |
| `no pg_hba.conf entry ... SSL off` (PostgreSQL) | `rds.force_ssl` is on (default 1 for RDS for PostgreSQL 15 and later, 0 for 14 and older); connect with SSL (`sslmode=require` or stronger) |
| certificate verification failure | client does not trust the DB's CA; use the RDS CA bundle (`global-bundle.pem`; the default CA is `rds-ca-rsa2048-g1`) and check the account/instance CA setting on the SSL page |
| `too many connections` | the engine's `max_connections` is reached; pool connections or use RDS Proxy |
| IAM authentication failure | the authentication token is valid for 15 minutes; check it has not expired and that the DB user is set up for IAM authentication |

## Verify
- [ ] Subnet group spans at least two AZs with spare IPs, in isolated subnets.
- [ ] `nc -vz` succeeds from each client tier; Reachability Analyzer shows reachable.
- [ ] Clients use TLS with the current CA bundle; connections succeed after a failover test.

## Checked
Date: 2026-10-27. Sources: RDS User Guide USER_VPC.WorkingWithRDSInstanceinaVPC (subnet and AZ requirements,
reserved IP, public subnets, IPv6), CHAP_Troubleshooting (can't connect causes, 169.254.0.0/16), UsingWithRDS.SSL (CA names,
default CA), PostgreSQL.Concepts.General.SSL (`rds.force_ssl` defaults and error text), UsingWithRDS.IAMDBAuth.Connecting
(15-minute token); botocore `rds` model (`DBSubnetGroupName` on ModifyDBInstance). Corrected `rds.force_ssl`
(default on from PostgreSQL 15); removed the unconfirmed subnet-group move/outage rules, cross-VPC security group
reference rule, PAM error text and the generic database-name row.
Method: documentation only; no commands were run.
