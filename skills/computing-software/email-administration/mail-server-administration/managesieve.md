---
id: computing-software.email-administration.mail-server-administration.managesieve
name: managesieve
category: computing-software
field: email-administration
product: mail-server-administration
tags: [managesieve, sieve-port-4190]
level: advanced
status: docs-checked
description: "Expose ManageSieve so users edit filters from their mail client, secured with TLS and the same auth."
sources:
  - https://doc.dovecot.org/2.3/configuration_manual/sieve/managesieve/configuration/
  - https://doc.dovecot.org/main/core/man/doveadm-sieve.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managesieve

**Goal:** user-editable Sieve over port 4190.
## Steps
1. Install Pigeonhole (it provides `managesieve` and `managesieve-login`); add `sieve` to `protocols`, e.g. `protocols = $protocols sieve`. The daemon listens on port 4190 by default.
2. `service managesieve-login { inet_listener sieve { port = 4190 } }` is the stock listener (commented out in 20-managesieve.conf).
3. Scripts uploaded this way go to the location set by the `sieve` plugin setting, default `file:~/sieve;active=~/.dovecot.sieve`.
4. Back up existing `.dovecot.sieve` files first; the docs warn that moving them into the Sieve storage is not well tested.
## Failure modes
- Exposing 4190 to the internet widens the attack surface; restrict by firewall.
- By default users may keep unlimited scripts; limit with `sieve_max_script_size`, `sieve_quota_max_scripts` and `sieve_quota_max_storage`.
## Verify
- A client with Sieve editing connects and saves; `doveadm sieve list -u alice@example.com` shows it.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 ManageSieve Configuration page (add sieve to protocols, port 4190, default sieve location, quota settings, backup warning), the Pigeonhole settings reference (`sieve_max_script_size`) and the doveadm-sieve man page (`sieve list -u`). Removed the claim that ManageSieve inherits the IMAP TLS settings (not stated).

Method: documentation only; no commands were run.
