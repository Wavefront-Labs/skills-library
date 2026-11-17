---
id: computing-software.email-administration.dovecot.authentication-penalty-brute-force-slowdown
name: authentication-penalty-brute-force-slowdown
category: computing-software
field: email-administration
product: dovecot
tags: [auth-penalty, anvil, nodelay, brute-force, login-trusted-networks, auth-failure-delay]
level: advanced
status: docs-checked
description: "How the anvil process delays repeated failed logins per IP: delay doubling, what is skipped, IPv6 /48 grouping and how to disable it."
sources:
  - https://doc.dovecot.org/main/core/config/auth/penalty.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The anvil process tracks authentication penalties per IP address to slow brute-force attempts. Each failed login raises the penalty up to a maximum, unless the passdb returns the `nodelay` extra field. The penalty is applied for the IP before passdb lookups, so delays can occur even for `nodelay` logins if not all attempts from that IP use it.

Timing: the first failure reply is delayed 2 seconds (this happens even without the penalty). The delay then doubles: 4, 8 seconds, and stops at a ceiling of 15 seconds. The limits are compile-time constants (`AUTH_PENALTY_MAX_SECS` and `AUTH_PENALTY_MAX_PENALTY` in `src/auth/auth-penalty.h`).

Exemptions and quirks:
- IPs in `login_trusted_networks` (webmail servers, for example) skip penalties entirely.
- If the username plus password matches one of the last 10 attempts, the penalty does not rise again. A user who simply mistyped a saved password should not escalate the delay. The comparison uses a CRC32, so rare collisions are possible.
- Parallel auth lookups from the same IP can still run at the same time.
- For IPv6 the entire /48 block is penalized together, which may be too broad for shared address space.

Penalty tracking can be switched off completely by setting `mode = 0` on the `anvil-auth-penalty` unix_listener of `service anvil`. Pair this with an external banning tool when you need real lockouts rather than delays, since a delay does not stop distributed guessing.

## Checked

2026-11-03. Confirmed on the Authentication Penalty page: anvil tracks penalties per IP, nodelay extra field, 2 s first delay then 4, 8 and a 15 s ceiling, the compile-time constants in auth-penalty.h, login_trusted_networks exemption, the last-10-attempts CRC32 rule, parallel lookups, the /48 IPv6 block, and disabling via `service anvil { unix_listener anvil-auth-penalty { mode = 0 } }`. Added the disabling setting; nothing removed.

Method: documentation only; no commands were run.
