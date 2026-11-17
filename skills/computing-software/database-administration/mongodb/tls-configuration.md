---
id: computing-software.database-administration.mongodb.tls-configuration
name: tls-configuration
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-security, mongodb-tls, tls-mode, requiretls, x509-certificates, cluster-file, cafile, encryption-in-transit]
level: practitioner
status: docs-checked
description: "Encrypt MongoDB client and intra-cluster traffic with TLS: net.tls settings, certificates for members, rolling from disabled to requireTLS, and client options."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/configure-ssl/
  - https://www.mongodb.com/docs/manual/tutorial/upgrade-cluster-to-ssl/
  - https://www.mongodb.com/docs/manual/reference/configuration-options/#net.tls-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS configuration

**Goal:** all connections to and between mongod/mongos are encrypted and server identity is verified.

## Server config
```yaml
net:
  port: 27017
  bindIp: <addresses clients and members use>   # defaults to localhost only
  tls:
    mode: requireTLS                          # disabled | allowTLS | preferTLS | requireTLS
    certificateKeyFile: <path to server PEM>  # certificate + private key; a SAN must match the hostname other members use
    CAFile: <path to CA PEM>                  # or set the tlsUseSystemCA parameter; the two are mutually exclusive
    clusterFile: <path to member PEM>         # optional separate cert for internal membership auth
    allowConnectionsWithoutCertificates: true # default false: clients must present certs; true = encrypt but do not require
    disabledProtocols: TLS1_0,TLS1_1          # comma-separated, no spaces after commas
```
Mode meanings: `disabled` no TLS; `allowTLS` accepts TLS and non-TLS inbound, server-to-server connections do not use TLS; `preferTLS` accepts both inbound, server-to-server uses TLS; `requireTLS` only TLS. If `clusterFile` is not set, internal auth uses `certificateKeyFile`. On Linux/BSD `certificateKeyFile` is required when TLS is enabled. If you use X.509 authentication, `CAFile` is required. If a certificate has an Extended Key Usage extension, `certificateKeyFile` must include `serverAuth` (and `clientAuth` too when `clusterFile` is omitted).

## Rolling upgrade to TLS without downtime
1. Every node: `net.tls.mode: allowTLS` plus certificate and CA settings, rolling restart.
2. Switch all clients to TLS.
3. On each node: `db.adminCommand({ setParameter: 1, tlsMode: "preferTLS" })` (now all connections use TLS).
4. On each node: `setParameter` `tlsMode: "requireTLS"`, then edit the config files so a restart keeps it.
(Alternatively restart each node with the new options instead of `setParameter`.)

## Clients
Connect with TLS enabled and a CA file (`tls=true` in the connection string or the matching `--tls*` options in the shell); present a client certificate with `--tlsCertificateKeyFile` for X.509 auth. `tlsAllowInvalidCertificates` and `tlsAllowInvalidHostnames` (server options `net.tls.allowInvalidCertificates` / `allowInvalidHostnames`, default false) disable verification: never use them in production.

## Certificate rotation
`db.adminCommand({ rotateCertificates: 1 })` (or `db.rotateCertificates()`) rotates certificates without a restart; existing connections keep the old certificates, new connections use the new. Before 5.0 rotation needed downtime. A bad, expired, revoked or missing certificate file makes rotation fail but leaves the current TLS configuration running. Not usable with `certificateSelector` set to a thumbprint. mongod/mongos log a warning when a presented X.509 certificate expires within 30 days.

## Gotchas
- Hostname mismatch is a top failure: a certificate SAN entry must match the hostname other members use (DNS names or IP addresses can be compared).
- On Windows, encrypted PEM files are not supported; use `certificateSelector`.
- FIPS mode: `net.tls.FIPSMode: true` (default false), needs a FIPS-compliant library and MongoDB Enterprise.

## Verify
Test a connection with `openssl s_client` against the member and confirm the certificate chain; a client without TLS is rejected in `requireTLS` mode.

## Checked
2026-10-31. Against the MongoDB manual pages Configure mongod and mongos for TLS/SSL, Upgrade a Cluster to Use TLS/SSL and the net.tls configuration options: mode values and semantics, `certificateKeyFile` / `clusterFile` / `CAFile` / `allowConnectionsWithoutCertificates` / `disabledProtocols` / `FIPSMode` behaviour and defaults, EKU rule, SAN matching, rolling-upgrade steps, certificate rotation behaviour and the 5.0 note, and the 30 day expiry warning. Removed unconfirmed details: example file names, the `db.serverStatus().transportSecurity` verification, exact connection-string and mongosh commands, the "mode changes from disabled need restart" note, and the O/OU/DC member-certificate rule.
Method: documentation only; no commands were run.
