---
id: computing-software.database-administration.valkey.security-model
name: security-model
category: computing-software
field: database-administration
product: valkey
tags: [security, protected-mode, requirepass, bind, authentication, firewall, injection]
level: practitioner
status: docs-checked
description: "Valkey security model: trusted-network design, bind and firewall, protected mode, ACL vs requirepass, TLS, malicious input (hash seed, SORT) and injection."
sources:
  - https://valkey.io/topics/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Valkey assumes trusted clients in trusted environments; never expose its port or socket to untrusted clients. Untrusted users should reach it only through an application layer that enforces ACLs and validates input. Report vulnerabilities to security@lists.valkey.io, not as a public issue.

Network: firewall the port so only application hosts connect. Bind to one interface with `bind 127.0.0.1`. An attacker with access can wipe everything with a single `FLUSHALL`.

Protected mode: with the default configuration (all interfaces, no password) Valkey answers only loopback clients and gives others an error explaining the fix. An admin can still disable it or bind everything.

Authentication: preferred method is ACL users. Legacy: `requirepass` in `valkey.conf` makes every unauthenticated query fail until `AUTH password`. Use a very long password because Valkey tests many guesses per second and nobody has to remember it; it is plain text in config and client settings. It is redundancy if the firewall fails, and `AUTH` is sent unencrypted without TLS, so it does not stop eavesdropping.

TLS covers clients, replication and the cluster bus.

Malicious input: hash functions use a per-execution random seed to prevent collision attacks that degrade O(1) to O(N). `SORT` uses non-randomised `qsort`, so crafted input can trigger quadratic behaviour.

Injection: the protocol uses length-prefixed binary-safe strings, so client libraries are not injectable; `EVAL` is equally safe, but do not build Lua bodies from untrusted strings.

Code: no root needed; run as an unprivileged `valkey` user.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/security/ (page text read in full): Trusted-environment model, firewall and bind 127.0.0.1, FLUSHALL risk, protected mode, ACLs as the recommended method, requirepass and AUTH, plain-text AUTH without TLS, TLS channels, hash seed, SORT qsort, protocol injection safety and EVAL, no root needed, security@lists.valkey.io.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
