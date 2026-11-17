---
id: computing-software.systems-network-administration.cisco-networking.napalm-getters-and-config-replace
name: napalm-getters-and-config-replace
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, napalm, napalm-getters, python, network-automation, config-replace, config-merge, compare-config, ios, nxos, eos]
level: practitioner
status: draft
description: "Use NAPALM with Cisco IOS/NX-OS: drivers, getters for normalised facts, load_merge vs load_replace, compare_config, commit/rollback and IOS prerequisites."
sources:
  - https://napalm.readthedocs.io/en/latest/
  - https://napalm.readthedocs.io/en/latest/support/ios.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NAPALM getters and config merge/replace

## Install and connect
```
pip install napalm
```
```python
from napalm import get_network_driver
driver = get_network_driver("ios")          # ios, nxos (NX-API), nxos_ssh, eos, junos, iosxr
dev = driver("10.0.0.1", "<USER>", "<PW>", optional_args={"secret": "<ENABLE>", "transport": "ssh"})
dev.open()
print(dev.get_facts())                       # vendor-neutral dict: hostname, model, os_version, serial
print(dev.get_interfaces_ip())
print(dev.get_bgp_neighbors())
print(dev.get_lldp_neighbors_detail())
```
Getters return the same structure across vendors; check the support matrix per getter/driver.

## Config changes
```python
dev.load_merge_candidate(config="ntp server 10.0.0.11\n")   # merge lines
# or full replacement:
dev.load_replace_candidate(filename="configs/r1.cfg")
print(dev.compare_config())                  # diff of candidate vs running
if diff_ok:
    dev.commit_config()                      # optionally revert_in=300 on supported drivers
else:
    dev.discard_config()
dev.rollback()                               # back to the pre-commit config
dev.close()
```

## IOS driver mechanics and prerequisites
- Candidate is copied to flash (SCP), `compare_config` uses `show archive config differences`,
  replace uses `configure replace flash:candidate_config.txt force`.
- Requires: `ip scp server enable`, `archive` configured (`archive path flash:archive`),
  privilege 15 user, enough flash.
- Full replace on IOS needs a **complete** config including crypto keys lines handled carefully;
  generate from a template that renders the whole device.

## Gotchas
- `configure replace` with differences in certificate/crypto sections can fail; test on lab copies.
- Getter output depends on parsing CLI for IOS; odd platforms may return partial data.
- Use NAPALM via Nornir or Ansible (`napalm` collection) for many devices with concurrency.

## Verify
- [ ] `compare_config()` empty after commit (idempotent); rollback tested in lab.
