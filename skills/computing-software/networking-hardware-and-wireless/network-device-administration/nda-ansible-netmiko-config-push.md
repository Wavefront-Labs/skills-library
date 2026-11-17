---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-ansible-netmiko-config-push
name: nda-ansible-netmiko-config-push
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [network-automation-ansible, netmiko-config-push, napalm-compare-config, nda-automation]
level: advanced
status: draft
description: "Push templated config with Ansible network modules, Netmiko or NAPALM using diff, dry-run and rollback guards."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safe automation

- Source of truth (YAML/NetBox/Git) plus Jinja2 templates generate per-device config.
- Netmiko: SSH library for CLI (`send_config_set`, `save_config`); NAPALM: `load_merge_candidate` then `compare_config` then `commit_config` with rollback support on supported platforms; Ansible: platform collections (e.g. `cisco.ios`, `junipernetworks.junos`) with `--check --diff`.
- Guard rails: run against a canary first, apply to a small batch, verify with pre/post checks (BGP neighbours, interface state), commit-confirmed on Junos, `reload in` on IOS-XE if no rollback.
- Store credentials in a vault; log runs.

## Verify
- [ ] A dry run on a lab device produces the expected diff and no change; a real run is followed by a passing post-check.
