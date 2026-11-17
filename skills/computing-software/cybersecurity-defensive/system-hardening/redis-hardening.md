---
id: computing-software.cybersecurity-defensive.system-hardening.redis-hardening
name: redis-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [database-hardening, redis-hardening, redis-acl, protected-mode, rename-command, redis-tls, exposed-redis]
level: practitioner
status: docs-checked
description: "Harden Redis: never internet-exposed, bind and protected mode, ACL users instead of one password, restricting dangerous commands, TLS, running unprivileged."
sources: ["https://redis.io/docs/latest/operate/oss_and_stack/management/security/", "https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/", "https://redis.io/docs/latest/operate/oss_and_stack/management/security/encryption/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis hardening

Redis is designed for trusted clients in trusted environments; exposing it to the internet is the core mistake.
Because `CONFIG` lets a client change the working directory and dump file name, an attacker with access can write
RDB files to arbitrary paths, which may lead to code execution as the Redis user.

## Network first
- Firewall the Redis port so only the application servers reach it; on a single internet-facing host, loopback
  clients still work.
- In `redis.conf`, bind to one interface, for example `bind 127.0.0.1`, or the private interface only. Do not bind
  all interfaces on a host with a public IP.
- Protected mode (since 3.2.0) applies when the default configuration (binding all interfaces) is used with no
  password: Redis then answers only loopback clients. An administrator can still disable it, so do not rely on it.
- Apply the same firewalling to the cluster bus and Sentinel ports.

## Authentication: ACLs (Redis 6+)
ACLs are the recommended method; `requirepass` is the legacy single shared password.
```
user default off
user app on >S3cretLongRandom ~app:* &app:* +@read +@write -@dangerous
user admin on >AnotherLongSecret ~* &* +@all
```
Out of the box the `default` user is `on nopass ~* &* +@all`, so new connections are authenticated automatically;
turn it off or give it a password. Load users from a file with `aclfile /etc/redis/users.acl`. Use long random
passwords, because Redis is fast and many guesses per second are possible. `AUTH` is sent unencrypted, so use TLS.

## Dangerous commands
`-@dangerous` removes the commands tagged dangerous, which include FLUSHALL, MIGRATE, RESTORE, SORT, KEYS, CLIENT,
DEBUG, INFO, CONFIG, SAVE and REPLICAOF. Note that command categories other than `+@all` never include module
commands. The older `rename-command CONFIG ""` is documented as deprecated; use ACL rules instead.

## TLS (Redis 6+, built with TLS support)
```
port 0
tls-port 6379
tls-cert-file /etc/redis/tls/redis.crt
tls-key-file /etc/redis/tls/redis.key
tls-ca-cert-file /etc/redis/tls/ca.crt
```
By default Redis requires clients to present a valid certificate (mutual TLS); `tls-auth-clients no` disables that.
The same directives apply to replication links.

## Host
Redis does not need root; run it as an unprivileged `redis` user used only for that purpose. Keep it patched.
Managed services still need auth, TLS and private networking.

## Detect abuse
Look for `CONFIG` changes of `dir` or the dump file name, unexpected keys holding cron or SSH key content,
outbound connections from the Redis host, and denied commands in the ACL log.

## Verify
From an untrusted network the port is closed. The app user gets a NOPERM error for commands outside its ACL, such
as `CONFIG`. Redis runs as the `redis` user.

## Checked
2026-10-31. Confirmed on the Redis security, ACL and encryption pages: untrusted-network warning, `bind`, protected
mode behaviour (3.2.0), ACLs as the recommended method from Redis 6, default user `on nopass ~* &* +@all`, `>password`
syntax, `-@dangerous` and its command list, module commands excluded from categories, `aclfile`, `rename-command`
deprecated, `tls-port`/`tls-ca-cert-file`/`tls-auth-clients no`, mutual TLS by default, unprivileged `redis` user,
NOPERM errors. Removed as not confirmed on those pages: specific cluster-bus and Sentinel port numbers, the
`enable-*-command` defaults, `tls-auth-clients optional`, systemd sandboxing and data-dir mode, Lua CVE remark,
the `ACL LOG` and `MODULE LOAD` specifics, and NOAUTH wording.
Method: documentation only; no commands were run.
