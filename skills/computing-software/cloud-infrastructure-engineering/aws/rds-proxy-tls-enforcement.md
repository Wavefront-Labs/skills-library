---
id: computing-software.cloud-infrastructure-engineering.aws.rds-proxy-tls-enforcement
name: rds-proxy-tls-enforcement
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds-proxy, proxy-tls, tls, amazon-root-ca, certificate-verification]
level: advanced
status: docs-checked
description: "Enforce TLS on RDS Proxy with RequireTLS, trust the Amazon Root CA (not the RDS CA bundle) for verify-full, and understand proxy-to-database encryption."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.howitworks.html#rds-proxy-security.tls", "https://www.amazontrust.com/repository/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS Proxy TLS enforcement

## 1. Require TLS
```bash
aws rds modify-db-proxy --db-proxy-name app-proxy --require-tls
aws rds describe-db-proxies --db-proxy-name app-proxy --query 'DBProxies[].RequireTLS'
```
The API describes `RequireTLS` as whether TLS encryption is required for connections to the proxy. (The User Guide
console text also describes the setting as enforcing TLS between the proxy and the database; test both directions
rather than assuming.) Clients can also require TLS themselves with `sslmode=require` (PostgreSQL) or `--ssl-mode`
(MySQL); by default clients establish an encrypted connection, and the proxy supports all client SSL modes.
With `RequireTLS` on, a client connecting with `sslmode=disable` (PostgreSQL) or `--ssl-mode=DISABLED` (MySQL) gets
`This RDS Proxy requires TLS connections` (MySQL error 3159, PostgreSQL 28000); connect with at least `--ssl-mode=REQUIRED`
(MySQL) or a non-disable `sslmode` (the User Guide names `allow` as the PostgreSQL minimum; prefer `require` or stronger),
or turn the setting off. IAM authentication through the proxy is allowed only over SSL connections.
The proxy supports TLS 1.0, 1.1, 1.2 and 1.3, and a client can use a higher TLS version than the database supports.

## 2. Trust the right CA
RDS Proxy uses certificates from AWS Certificate Manager (ACM), so you do not need the RDS certificate bundle for
the proxy. For `VERIFY_CA` or `VERIFY_IDENTITY` (MySQL) or `verify-full` (PostgreSQL), the User Guide says to download all
root CA PEMs from Amazon Trust Services (https://www.amazontrust.com/repository/) and place them into a single
`.pem` file, then point the client at it:
```bash
psql "host=app-proxy.proxy-xxxx.<REGION>.rds.amazonaws.com dbname=app user=app sslmode=verify-full sslrootcert=amazon-roots.pem"
mysql -h app-proxy.proxy-xxxx.<REGION>.rds.amazonaws.com -u app -p --ssl-mode=VERIFY_IDENTITY --ssl-ca=amazon-roots.pem
```
The `psql` `sslrootcert` form follows the PostgreSQL client convention rather than a User Guide example. A combined
bundle (RDS CA bundle plus Amazon roots) lets one config talk to both the proxy and the DB directly.

## 3. Hostname
RDS Proxy uses wildcard certificates (covering the domain and its subdomains), so verify against the proxy endpoint
name (or custom proxy endpoints), not a CNAME you own unless the client verifies the real endpoint name. For the
`mysql` client with `VERIFY_IDENTITY`, the User Guide says to use the MySQL 8.0-compatible client.

## Verify
- [ ] A `verify-full` / `VERIFY_IDENTITY` connection through the proxy succeeds with the Amazon roots file, and a
  plaintext attempt (`sslmode=disable` / `--ssl-mode=DISABLED`) behaves as your `RequireTLS` setting intends. The User
  Guide notes SSL session variables are not set for connections through the proxy, so do not rely on server-side SSL status views to prove TLS.

## Checked
Date: 2026-10-27. Sources: RDS User Guide rds-proxy.howitworks (Using TLS/SSL with RDS Proxy: ACM certificates,
Amazon Trust Services roots, wildcard certificates, TLS 1.0-1.3, client SSL modes); botocore `rds` model
(`RequireTLS` on CreateDBProxy, ModifyDBProxy, DBProxy). Also read rds-proxy.troubleshooting (error text for `RequireTLS` and IAM-over-SSL).
Removed the Amazon Root CA 1 chain claim and the `rds.force_ssl` claim (not stated in the documentation read).
Method: documentation only; no commands were run.
