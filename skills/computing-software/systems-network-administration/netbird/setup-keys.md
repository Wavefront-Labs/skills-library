---
id: computing-software.systems-network-administration.netbird.setup-keys
name: setup-keys
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, setup-keys, one-off-key, reusable-key, ephemeral-peers, auto-groups]
level: practitioner
status: docs-checked
description: "Create and use NetBird setup keys for unattended peer registration: one-off versus reusable, expiry, usage limits, auto-assigned groups, ephemeral peers and caveats."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/register-machines-using-setup-keys.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Types: a one-off key authenticates one machine and cannot be reused; a reusable key authenticates many machines up to a usage limit. One-off is recommended for security.

Create under Settings > Setup Keys (or Peers > Add Peer > Generate Key). Options:
- Expiration: dialog pre-fills 7 days; empty means never.
- Usage limit: reusable keys are unlimited by default; set a limit (e.g. 30 for 30 machines).
- Auto-assign groups: every peer registered with the key joins these groups so access rules apply immediately.
- Ephemeral peers: removed after being offline more than 10 minutes; suits containers and autoscaling.
- Allow Extra DNS Labels: lets peers use `--extra-dns-labels`.

Use on each machine: `netbird up --setup-key <SETUP KEY>`.

The quick Generate Key in Add Peer makes a one-off key expiring in 24 hours with no auto groups.

Caveats:
- Revoking or expiry does not disconnect machines already authenticated.
- Auto-groups apply only to newly registered machines.
- Ephemeral peers get an IP-based DNS suffix (e.g. `ci-runner-12-7.netbird.cloud`) unless Reject Hostname Collisions is on; with it on, a peer whose name is taken fails to register.
- Peers sharing an extra DNS label form a round-robin group.

## Checked

2026-11-04. Confirmed against the NetBird setup keys page: key types, 7-day default expiry, unlimited reusable usage, auto-assign groups, ephemeral 10-minute removal, extra DNS labels, `netbird up --setup-key`, Generate Key defaults, revoke and expiry behaviour, hostname collision caveat. Nothing removed.
Method: documentation only; no commands were run.
