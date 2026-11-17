---
id: computing-software.networking-hardware-and-wireless.strongswan.charon-cmd-client
name: charon-cmd-client
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, charon-cmd, command-line-client, auth-profiles, roadwarrior]
level: practitioner
status: docs-checked
description: "Start an IKE VPN client from the command line with charon-cmd: required host and identity options, credential flags, proposals, traffic selectors and authentication profiles."
sources:
  - https://docs.strongswan.org/docs/latest/daemons/charon-cmd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# charon cmd client
`charon-cmd --host <hostname> --identity <id> [options]` sets up IKEv1 and IKEv2 IPsec VPN connections for road-warrior scenarios. Like charon it must run as root or as a user with CAP_NET_ADMIN. `--host` and `--identity` are required; other credentials depend on the profile. Many strongswan.conf charon options apply; for example, put a `filelog` section with a `stdout` logger (`default = 1`, `ike = 2`, `cfg = 2`) inside a `charon-cmd` section of strongswan.conf.

**Options.**
- `--debug <level>` (-1 to 4, default 1)
- `--remote-identity` (default: host)
- `--eap-identity`, `--xauth-username`
- Credentials: `--cert <path>` (repeatable), `--rsa`, `--priv`, `--p12`, `--agent[=<socket>]` (SSH agent, socket from SSH_AUTH_SOCK by default)
- `--local-ts` (extra local selector; the virtual IP is always proposed), `--remote-ts` (default 0.0.0.0/0)
- `--ike-proposal`, `--esp-proposal`, `--ah-proposal` (one proposal replacing defaults)
- `--childless[=force]` (force aborts if the responder lacks support)
- `--profile <name>`

**Profiles.** Default is `ikev2-pub` if a private key is supplied, otherwise `ikev2-eap`.
- IKEv2: `ikev2-pub`, `ikev2-eap` (EAP client, public key server), `ikev2-pub-eap` (RFC 4739, both), `ikev2-psk`
- IKEv1 main mode: `ikev1-pub`, `ikev1-xauth`, `ikev1-xauth-psk`, `ikev1-hybrid` (server public key, then XAuth)
- IKEv1 aggressive mode: `ikev1-pub-am`, `ikev1-xauth-am`, `ikev1-xauth-psk-am` (marked INSECURE), `ikev1-hybrid-am`

## Checked
2026-11-04. Confirmed against the charon-cmd page of the strongSwan docs: synopsis, required options, every option and default listed, and all authentication profile names. Removed the claim that no config files are used (not on the page).

Method: documentation only; no commands were run.
