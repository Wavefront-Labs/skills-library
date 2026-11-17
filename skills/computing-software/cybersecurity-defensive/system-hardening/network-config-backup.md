---
id: computing-software.cybersecurity-defensive.system-hardening.network-config-backup
name: network-config-backup
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [network-device-hardening, network-config-backup, oxidized, rancid, config-diff, golden-config, disaster-recovery]
level: practitioner
status: draft
description: "Back up network device configurations automatically with Oxidized or RANCID into Git, alert on unexpected diffs, protect the backups and test restores."
sources: ["Oxidized project documentation", "NIST SP 800-53 Rev 5 CM-2 Baseline Configuration and CP-9 System Backup", "CIS Controls v8 - Safeguard 4.2 and 11.2"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network configuration backup

**Goal:** every network device's running config is versioned off-box daily, changes are visible, and restore is proven.

## Oxidized (common choice)
`~/.config/oxidized/config`:
```yaml
interval: 3600
input:
  default: ssh
  ssh: { secure: true }
source:
  default: csv
  csv: { file: ~/.config/oxidized/router.db, delimiter: !ruby/regexp /:/, map: {name: 0, model: 1, group: 2} }
output:
  default: git
  git: { user: oxidized, email: oxidized@corp.example, repo: ~/oxidized.git }
hooks:
  push_to_remote:
    type: githubrepo
    events: [post_store]
    remote_repo: git@git.corp.example:netops/configs.git
```
`router.db`: `core-sw1:ios:core`. Use a dedicated read-only TACACS+ account (privilege needed to `show running-config`) with SSH keys where supported.
Alternatives: RANCID (CVS/Git, older), vendor tools (Cisco Prime/DNA Center, Panorama, FortiManager), Ansible `*_config` backup modules, NetBox + Nornir.

## Change detection
- Git diff notifications to the network team channel; correlate with change tickets.
- Diffs on devices with no open change = possible unauthorised change or compromise; investigate.
- Compare against golden templates (Batfish, Nornir compliance tasks) to catch drift.

## Protect the backups
Configs contain password hashes, SNMP and VPN keys: restrict repo access, encrypt at rest, consider stripping secrets (`remove_secret: true` in Oxidized) for the general repo plus a sealed full copy.

## Restore test
Quarterly: restore a config to a lab device or virtual image (CML/EVE-NG) and confirm it boots and passes basic checks. Record device model/OS version with each backup, since configs may not apply across versions.

## Verify
- [ ] Every device in inventory has a backup newer than 24 h (Oxidized `/nodes` status or report).
- [ ] Repo access limited to network and security teams.
