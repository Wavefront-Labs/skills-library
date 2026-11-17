---
id: computing-software.systems-network-administration.virtualisation.proxmox-tfa-and-root-lockout-recovery
name: proxmox-tfa-and-root-lockout-recovery
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [tfa-recovery, pve-tfa, pveum, totp, root-lockout, proxmox]
level: practitioner
status: docs-checked
description: "Recover Proxmox VE GUI access after a lost TOTP/WebAuthn device or forgotten password: recovery keys, removing TFA via shell, resetting PAM and PVE realm passwords."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pveum.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TFA and root lockout recovery

## Prevent first
- Every TFA user: generate **recovery keys** (single-use recovery keys, a supported TFA method) and store them in the vault.
- Keep two admins with TFA, plus console (IPMI) access for root.

## Lost TFA device, user has shell access (root@pam on the node)
An administrator can remove a user's TFA entries from the GUI; the admin guide's user management chapter describes the options.
TFA config is stored cluster-wide in `/etc/pve/priv/tfa.cfg`; editing it by hand is a
last resort (back it up first).

## Forgotten passwords
| Realm | Reset |
|---|---|
| `root@pam` / any `@pam` | it's the Linux password: `passwd root` on the node (console/SSH) |
| `@pve` | `pveum passwd alice@pve` (run as root) |
| LDAP/AD/OpenID | reset at the identity provider |

No root shell at all: use the out-of-band console and the standard Debian root password recovery procedure (boot to a recovery shell, `passwd root`, reboot).

## Realm-enforced TFA
Realms can require TFA (`tfa type=oath` on the realm, older style) or per-user. If a realm
TFA requirement locks everyone out, edit the realm from a root shell with `pveum realm modify` (the `--tfa` option is described in the admin guide).

## Gotchas
- Webauthn entries are bound to the GUI origin (hostname); accessing by IP or a new FQDN
  makes keys fail. Configure the WebAuthn settings (rp, origin) in `/etc/pve/datacenter.cfg`.
- Locked out after repeated failed TFA attempts? Unlock with `pveum user tfa unlock <userid>`.

## Verify
User logs in with password and new TFA enrolled; recovery keys regenerated and stored;
audit shows the expected TFA entries for admins.

## Checked

2026-10-28

Confirmed: Admin guide user management chapter: TFA methods incl. recovery keys, priv/tfa.cfg, pveum passwd, pveum user tfa unlock, realm --tfa type option, webauthn rp/origin in datacenter.cfg.

Removed or corrected: pveum user tfa list/delete commands, the wrong claim that PVE has no TFA lockout, init=/bin/bash procedure, GUI menu paths, fail2ban, the realm TFA clear command.

Method: documentation only; no commands were run.
