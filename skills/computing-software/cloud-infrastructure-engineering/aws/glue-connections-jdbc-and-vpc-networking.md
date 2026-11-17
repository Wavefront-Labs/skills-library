---
id: computing-software.cloud-infrastructure-engineering.aws.glue-connections-jdbc-and-vpc-networking
name: glue-connections-jdbc-and-vpc-networking
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, glue, glue-connection, jdbc, glue-vpc, self-referencing-security-group, secrets-manager]
level: practitioner
status: docs-checked
description: "Connect AWS Glue jobs and crawlers to databases in a VPC: JDBC and network connections, subnet and security group placement, VPC DNS settings and secrets."
sources: ["https://docs.aws.amazon.com/glue/latest/dg/glue-connections.html", "https://docs.aws.amazon.com/glue/latest/dg/getting-started-vpc-config.html", "https://docs.aws.amazon.com/glue/latest/dg/set-up-vpc-dns.html", "https://docs.aws.amazon.com/glue/latest/dg/connection-properties.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Glue connections: JDBC and VPC networking

## Create
```bash
aws glue create-connection --connection-input '{
  "Name":"orders-pg","ConnectionType":"JDBC",
  "ConnectionProperties":{"JDBC_CONNECTION_URL":"jdbc:postgresql://orders.cluster-abc.eu-west-1.rds.amazonaws.com:5432/orders",
                          "SECRET_ID":"glue/orders-pg","JDBC_ENFORCE_SSL":"true"},
  "PhysicalConnectionRequirements":{"SubnetId":"subnet-priv-a","AvailabilityZone":"eu-west-1a",
                                    "SecurityGroupIdList":["sg-glue"]}}'
```
- `ConnectionType` enum includes `JDBC`, `NETWORK` (VPC placement only), `KAFKA`, `MONGODB`,
  `MARKETPLACE`, `CUSTOM` and many SaaS/database-specific types (botocore model).
- Credentials: `SECRET_ID` is a valid `ConnectionPropertyKey`; the job role needs permission to read the secret.
  A BASIC secret stores `username` and `password`.
- `JDBC_ENFORCE_SSL`, `JDBC_DRIVER_JAR_URI` and `JDBC_DRIVER_CLASS_NAME` are valid connection property keys.

## Networking rules
- Place the connection in a subnet whose route table reaches the data store; with several data stores in one
  job, they must be in the same subnet or reachable from it.
- For sources outside AWS, the VPC guide describes a NAT gateway with a public subnet for the external
  connection and a private subnet for the job.
- Enable both `enableDnsHostnames` and `enableDnsSupport` on the VPC.
- Database security group allows the database port from the Glue security group.
- `PhysicalConnectionRequirements` takes `SubnetId`, `AvailabilityZone` and `SecurityGroupIdList`.

## Test
Console connection test, or run a tiny job reading one table. For timeouts check the security groups,
network ACLs and routing.

## Use in jobs
- Jobs list the connection (`--connections orders-pg`).

## Verify
- [ ] Test connection succeeds; job reads a sample table and writes to S3.
- [ ] VPC DNS attributes enabled; database security group allows the Glue security group.

## Checked

2026-10-28. Confirmed against AWS documentation: ConnectionType and ConnectionPropertyKey enums, PhysicalConnectionRequirements members (botocore glue model), VPC DNS attributes, same-subnet rule, NAT/public-private guidance, BASIC secret username/password.
Removed: self-referencing rule text and error strings, S3 endpoint advice, custom driver/extra-jars, crawler path and hashfield tuning, Test connection console path; replaced prose-only sources with URLs.
Method: documentation only; no commands were run.
