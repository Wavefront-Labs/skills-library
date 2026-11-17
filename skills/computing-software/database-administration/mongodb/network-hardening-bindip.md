---
id: computing-software.database-administration.mongodb.network-hardening-bindip
name: network-hardening-bindip
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-security, bindip, network-hardening, firewall, ip-allowlist, exposed-database]
level: practitioner
status: docs-checked
description: "Limit MongoDB network exposure: net.bindIp, firewall rules for app and member traffic, disabling unneeded interfaces, and checking a deployment is not open to the internet."
sources:
  - https://www.mongodb.com/docs/manual/core/security-mongodb-configuration/
  - https://www.mongodb.com/docs/manual/administration/security-checklist/
  - https://www.mongodb.com/docs/manual/reference/configuration-options/#net-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network hardening (bindIp and firewalls)

A MongoDB instance reachable from untrusted networks is a major risk. Defence in depth: bind narrowly, firewall, and require auth + TLS.

## bindIp
`net.bindIp` defaults to `localhost`; the command-line `--bind_ip` overrides the config file, and `net.bindIp` and `net.bindIpAll` are mutually exclusive.
```yaml
net:
  port: 27017
  bindIp: localhost,10.0.12.5            # loopback + private interface only
  # bindIpAll: true                      # avoid; listens on every interface (same as 0.0.0.0)
  ipv6: false
  maxIncomingConnections: 20000
```
`bindIp` accepts IP addresses, hostnames and Unix domain socket paths; IPv6 addresses also require `net.ipv6: true`. The manual advises DNS hostnames rather than IP addresses when configuring replica set or sharded cluster members. Do not bind a public interface. In containers, bind `0.0.0.0` inside the container but publish the port only on a private network.

## Firewall rules
Allow only:
- application hosts / mongos -> mongod/mongos port (27017, or 27018 for shards, 27019 config)
- replica set members <-> each other on their ports
- monitoring / backup agents
Deny everything else, including from the internet. The manual's security checklist says to run MongoDB in a trusted network and use firewalls or security groups to control inbound and outbound traffic; `security.clusterIpSourceAllowlist` and the `authenticationRestrictions` field of `db.createUser()` add per-source restrictions.

## Other settings
```yaml
security:
  authorization: enabled                 # never run network-reachable without it
net:
  tls: { mode: requireTLS, certificateKeyFile: ..., CAFile: ... }
setParameter:
  enableLocalhostAuthBypass: false       # startup parameter; the localhost exception is enabled by default
```
- `net.unixDomainSocket.filePermissions` (default 0700) controls access to the Unix domain socket on shared hosts.

## Check exposure
```bash
ss -ltnp | grep mongo                                    # what is listening where
mongosh "mongodb://<public-ip>:27017" --eval 'db.runCommand({ping:1})'   # from outside: must fail to connect
```
Query `db.adminCommand({ getCmdLineOpts: 1 }).parsed.net` to confirm effective settings.

## Verify
From an unauthorized network the TCP connection is refused/times out; from an app host a
connection without credentials can connect but `show dbs` fails with an authorization error.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: net.bindIp default localhost, comma-separated addresses and Unix socket paths, IPv6 needs net.ipv6 true, bindIp and bindIpAll mutually exclusive, --bind_ip overrides the config file, default ports 27017/27018/27019, enableLocalhostAuthBypass startup parameter (default true), net.unixDomainSocket.filePermissions default 0700, security.clusterIpSourceAllowlist, authenticationRestrictions, the security checklist advice on trusted networks and firewalls, DNS hostnames preferred for cluster members. Removed unconfirmed history claims, the REST/HTTP interface note and Atlas networking claims.

Method: documentation only; no commands were run.
