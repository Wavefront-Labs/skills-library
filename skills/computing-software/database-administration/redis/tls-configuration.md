---
id: computing-software.database-administration.redis.tls-configuration
name: tls-configuration
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-security, redis-tls, tls-port, tls-replication, tls-cluster, mutual-tls, rediss, encryption-in-transit]
level: practitioner
status: docs-checked
description: "Enable TLS in Redis 6+ for clients, replication and cluster bus: tls-port, certificates, optional client cert auth, and connecting with redis-cli and rediss:// URLs."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/security/encryption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis TLS

**Goal:** all Redis traffic (clients, replicas, cluster bus, Sentinel) is
encrypted, and clients verify the server.

## Build/package
TLS is optional and needs Redis built with `make BUILD_TLS=yes` (OpenSSL development libraries required).

## redis.conf
```
port 0                              # disable plaintext entirely (or keep for a migration window)
tls-port 6379
tls-cert-file /etc/redis/tls/redis.crt
tls-key-file  /etc/redis/tls/redis.key
tls-ca-cert-file /etc/redis/tls/ca.crt
tls-auth-clients optional           # yes = require client certs (mTLS); no = server-auth only
tls-protocols "TLSv1.2 TLSv1.3"
tls-replication yes                 # replica -> primary connections use TLS
tls-cluster yes                     # cluster bus uses TLS
```
Sentinel: `tls-replication yes` makes Sentinel use TLS to the masters and also enables TLS on its own port (Sentinel is configured with `tls-port` if and only if `tls-replication` is on).

## Clients
```bash
redis-cli --tls -h redis.example.com -p 6379 --cacert ca.crt \
  [--cert client.crt --key client.key] --user app -a "$APP_PW"   # --askpass prompts for the password instead
```
Client libraries configure TLS in their own way: check each library's documentation for the CA,
client certificate and hostname verification settings.

## Rotation
Certificate paths are ordinary `tls-*-file` settings: check the self-documented redis.conf for your version before relying on runtime reload, and renew certificates before expiry.

## Gotchas
- TLS lowers the throughput one instance can deliver; I/O threading with TLS is supported from Redis 8.0. Pool connections rather than reconnecting often.
- `tls-auth-clients` defaults to `yes`: clients without certs fail with handshake
  errors unless you set `optional`/`no`.

## Verify
`openssl s_client -connect redis.example.com:6379 -CAfile ca.crt` completes the
handshake; `redis-cli -p 6379 PING` without `--tls` fails; `INFO replication`
shows replicas connected after enabling `tls-replication`.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the Redis TLS page and redis.conf 8.2: `make BUILD_TLS=yes`; `port 0` with `tls-port 6379`; `tls-cert-file`, `tls-key-file`, `tls-ca-cert-file`; mutual TLS is the default (`tls-auth-clients` yes; `no` and `optional` also exist); `tls-replication yes` on replicas; `tls-cluster yes` for the cluster bus; Sentinel inherits TLS settings and uses `tls-port` iff `tls-replication` is enabled; `tls-protocols` defaults to TLSv1.2 and TLSv1.3; redis-cli flags `--tls`, `--cacert`, `--cert`, `--key`, `--user` (needs `-a`), `--askpass`; TLS lowers per-instance throughput and I/O threading with TLS is supported from 8.0. Removed unconfirmed: distro and Docker TLS build claims, rediss URL and hostname verification advice, runtime certificate reload, managed-service remarks.
Method: documentation only; no commands were run.
