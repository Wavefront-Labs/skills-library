---
id: computing-software.cybersecurity-defensive.system-hardening.tacacs-plus-network-aaa
name: tacacs-plus-network-aaa
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [network-device-hardening, tacacs, tacacs-plus, aaa, command-authorization, command-accounting, local-fallback]
level: advanced
status: docs-checked
description: "Centralise network device admin access with TACACS+: AAA authentication, per-command authorization and accounting, local fallback, server redundancy, and protecting the transport."
sources: ["https://datatracker.ietf.org/doc/html/rfc8907", "https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TACACS+ for network device AAA

TACACS+ (RFC 8907) is used mainly for device administration: authenticating access to network devices, centrally
authorizing operations (including per-command authorization) and auditing them (accounting).

## Protect the transport
RFC 8907 section 10 states that TACACS+ has no security mechanism meeting modern requirements: the packet-body
protection (an MD5-derived pad keyed by the shared secret) is "obfuscation", not encryption, with no meaningful
integrity, privacy or replay protection, and no forward secrecy. An attacker on the path should be assumed able to read
and modify packets, which could alter accounting records or authorization results. Users MUST limit access to known
clients and control the security of the whole transmission path (management network, out-of-band, or a secured
transport). Cisco's hardening guide describes TACACS+ as encrypting the whole payload (unlike RADIUS, which only
encrypts the password); treat that as a reason to prefer TACACS+ over RADIUS, not as a substitute for a protected
path. Never run in unencrypted-flag mode in production (the RFC says it MUST NOT be used).

## Cisco IOS configuration (from Cisco's hardening guide)
```
aaa new-model
aaa authentication login default group tacacs+ enable
tacacs-server host <TACACS_IP>
tacacs-server key <key>
enable secret <password>
!
aaa authorization exec default group tacacs none
aaa authorization commands 0 default group tacacs none
aaa authorization commands 1 default group tacacs none
aaa authorization commands 15 default group tacacs none
!
aaa accounting exec default start-stop group tacacs
aaa accounting commands 0 default start-stop group tacacs
aaa accounting commands 1 default start-stop group tacacs
aaa accounting commands 15 default start-stop group tacacs
!
username breakglass privilege 15 algorithm-type scrypt secret <strong>
```
- A method list is tried in order; later methods are used only if earlier ones fail due to server unavailability or
  misconfiguration, not when a server rejects the user.
- Fallback options for on-device authentication are `enable`, `local` and `line`. Cisco prefers the enable secret
  because it is hashed one way; local users give per-admin accountability during an outage at the cost of
  maintaining accounts on every device.
- Authorization examples end in `none`, which lets commands through if the AAA server is unreachable; choose
  deliberately.
- Command accounting sends the command, date and username to the TACACS+ server; it is not supported with RADIUS.
- Syntax varies by release; take exact commands from your platform documentation.

## Authorization design (server side)
- Map directory groups to roles (read-only, read-write, audit).
- Use command sets that allow or deny command patterns per role.
- Separate shared keys per device group, long and random.

## Accounting and audit
Every command with user, device, timestamp is logged on the TACACS+ server; forward to the SIEM and alert on
config changes outside change windows, use of the local break-glass account, and failed authorizations.

## Fallback and resilience
- Run redundant AAA servers so interactive management access (SSH) still works if one is unavailable.
- Local break-glass account: unique per device or vaulted, strong secret (type 9 scrypt per Cisco), use alerts.
- Keep an out-of-band console path for when AAA is broken.

## Gotchas
- Lockout risk: test with a second session open before saving.
- Type 7 passwords and keys are reversible obfuscation; protect configs and backups.
- Other vendors map privileges differently (vendor attributes or roles); test each platform.

## Verify
Login with a directory account succeeds via TACACS+, a read-only user is denied configuration commands, commands
appear in TACACS+ accounting logs, and with all servers unreachable only the fallback account works.

## Checked
2026-10-31. Confirmed in RFC 8907 (scope, section 10.1 obfuscation language, MD5 pad, unencrypted-flag rule, MUST
limit access and secure the path) and Cisco's hardening guide (AAA examples, method-list and fallback behaviour,
command authorization/accounting, redundant servers, type 7/type 9). Corrected: the previous text said TACACS+
"encrypts the whole payload"; the RFC calls it obfuscation. Removed: `ip tacacs source-interface`, `single-connection`,
named server products, MFA proxy claims, `if-authenticated`, `no aaa authorization console` and the Junos/PAN-OS/
FortiOS vendor-attribute specifics (not on the cited pages).
Method: documentation only; no commands were run.
