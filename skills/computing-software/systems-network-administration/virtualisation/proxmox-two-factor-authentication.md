---
id: computing-software.systems-network-administration.virtualisation.proxmox-two-factor-authentication
name: proxmox-two-factor-authentication
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-tfa, totp, webauthn, yubikey, recovery-keys, tfa-lockout, pveum, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Enforce two-factor login on Proxmox VE: TOTP, WebAuthn/FIDO2 and recovery keys per user, realm-enforced TFA, lockout limits, and recovering a user who lost their token."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_tfa_auth
  - https://github.com/proxmox/pve-docs/blob/master/pveum.adoc
  - https://github.com/proxmox/pve-access-control/blob/master/src/PVE/CLI/pveum.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Two-factor authentication on Proxmox VE

**Goal:** stolen passwords alone can't log in to the hypervisor management plane.

## Factors
| Factor | Notes |
|---|---|
| TOTP | Time-based one-time password (HMAC-SHA1, configurable time step and length); any authenticator app |
| WebAuthn (FIDO2) | Needs a trusted HTTPS certificate and the WebAuthn settings (Datacenter -> Options -> WebAuthn Settings, stored as `webauthn: rp=...,origin=...,id=...` in `/etc/pve/datacenter.cfg`); changing them may invalidate existing registrations |
| Recovery keys | Single-use codes; only one set per user at a time |
| Yubico OTP | Realm-enforced only; needs a Yubico API ID, key and validation server |
| U2F | Legacy; existing factors still work, WebAuthn is recommended |
Users add factors via the TFA button in the user list; admins use Datacenter -> Permissions -> Two Factor. Users can always add recovery keys.

## Enforce
- Per realm: set the **TFA** option of the realm (TOTP or Yubico OTP). Once set it is a requirement and only users with configured TFA can log in, so add keys to new users immediately.
- Realms that authenticate through an OpenID provider rely on that provider for MFA.
- Prioritise `root@pam` and every admin-role user.

## Lockout behaviour
For TOTP, 8 failed attempts disable the user's TOTP factors; a recovery key unlocks them. For WebAuthn and recovery keys the limit is 100 tries, after which all second factors are blocked for an hour. An admin can unlock at any time in the user list or with `pveum user tfa unlock <user>@<realm>`.

## Lost token
An admin removes the user's TFA entries (Datacenter -> Permissions -> Two Factor), and the user enrols again; from a node shell: `pveum user tfa delete <user>@<realm>` (all entries if no ID is given). User and TFA data live in the cluster file system, so this needs a writable `/etc/pve`.

## Gotchas
- WebAuthn is tied to the configured relying-party ID and origin: reach the GUI under that exact name, since a valid domain with a valid certificate is required.
- Changing the WebAuthn configuration may make all existing registrations unusable.

## Verify
Every admin account shows at least one TFA entry plus recovery keys; a login without the second factor fails.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and pve-access-control source (pveum CLI `tfa` commands).

Confirmed: realm-enforced TFA (TOTP, Yubico OTP) and its consequence, TOTP algorithm and configurability, WebAuthn requirements and `datacenter.cfg` syntax, recovery key rules, U2F being legacy, lockout limits (8 TOTP failures; 100 for WebAuthn and recovery keys with a one-hour block), `pveum user tfa unlock`, `pveum user tfa delete` (all entries when no ID given). Removed as unconfirmed: the 'PVE 7.2+' and '7.4+' version gates, the claim that API tokens bypass TFA, the `/etc/pve/priv/tfa.cfg` backup advice, the time-skew remark and the 'platform passkeys' wording.

Method: documentation only; no commands were run.
