---
id: computing-software.database-administration.yugabytedb.security-checklist-for-production
name: security-checklist-for-production
category: computing-software
field: database-administration
product: yugabytedb
tags: [security, checklist, hardening, network-exposure, rpc-bind-addresses, least-privilege, tls, rbac]
level: practitioner
status: docs-checked
description: "Production hardening checklist for YugabyteDB: authentication, RBAC, a dedicated OS user, restricted network exposure, TLS, and encryption at rest."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/security-checklist.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Security checklist for production

Work through these before exposing a cluster:

1. **Authentication.** Enable authentication so every client provides valid credentials.
2. **RBAC.** Grant users and applications only the privileges they need through roles; an administrator role is created first and creates the other roles.
3. **Dedicated OS user.** Run YB-Master and YB-TServer with a dedicated operating system account that can access the data drives but has no unnecessary permissions.
4. **Limit network exposure.**
   - Only application servers and database administrators should reach the servers, and only application servers should connect on the RPC ports.
   - List just the required interfaces in `--rpc_bind_addresses` when starting yb-master and yb-tserver; do not bind to the loopback address.
   - On public clouds avoid public IP addresses where possible, and keep security groups very restrictive, exposing only the client-accessible ports to the servers that need them. On AWS, run the cluster in a separate VPC peered only with the VPCs that need database access.
5. **Encryption in transit.** Use TLS for intra-cluster and client-to-server traffic.
6. **Encryption at rest.** Use a self-generated symmetric key for cluster-wide encryption.

## Checked

2026-11-04. Confirmed against the Security checklist page: the listed topics, dedicated OS user, --rpc_bind_addresses without loopback, no public IPs where possible, restrictive security groups, TLS and encryption at rest. Removed flag names, port numbers, scram, pgaudit, broadcast address and hba advice, which that page does not state.

Method: documentation only; no commands were run.
