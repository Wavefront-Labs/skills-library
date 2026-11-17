---
id: computing-software.systems-network-administration.cisco-networking.nornir-inventory-driven-automation
name: nornir-inventory-driven-automation
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [nornir, python, network-automation, inventory, netmiko, napalm, parallel-execution]
level: practitioner
status: draft
description: "Run Python network automation at scale with Nornir: YAML inventory with groups and defaults, threaded tasks via netmiko/napalm plugins, filtering and result handling."
sources:
  - https://nornir.readthedocs.io/en/latest/
  - https://github.com/ktbyers/nornir_netmiko
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nornir inventory-driven automation

Nornir is a Python framework (not a DSL): inventory + threaded task runner + plugins.

## Inventory (SimpleInventory)
```yaml
# hosts.yaml
sw1: {hostname: 10.99.0.21, groups: [ios_access], data: {site: syd}}
sw2: {hostname: 10.99.0.22, groups: [ios_access], data: {site: mel}}
# groups.yaml
ios_access: {platform: ios, data: {role: access}}
# defaults.yaml
username: netadmin
```
```yaml
# config.yaml
inventory: {plugin: SimpleInventory, options: {host_file: hosts.yaml, group_file: groups.yaml, defaults_file: defaults.yaml}}
runner: {plugin: threaded, options: {num_workers: 20}}
```
NetBox inventory plugin (`nornir_netbox`) replaces YAML with the source of truth.

## Task
```python
import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.password = os.environ["NET_PASSWORD"]
syd = nr.filter(F(site="syd") & F(groups__contains="ios_access"))

def ntp(task):
    task.run(netmiko_send_config, config_commands=["ntp server 10.99.0.5"])
    task.run(netmiko_send_command, command_string="show ntp associations")

r = syd.run(task=ntp)
print_result(r)
print("failed:", list(r.failed_hosts))
```

## Practice
- Dry run first: `nornir_napalm` `napalm_configure` with `dry_run=True` shows diffs.
- `num_workers` limits concurrency; AAA servers and slow devices dictate a sane value.
- Failed hosts do not stop the run; always report `r.failed_hosts` and rerun only those
  (`nr.data.failed_hosts`, `on_failed=True`).
- Keep secrets out of inventory files.

## Verify
- [ ] Run against a filtered test group first; results show no failed hosts; diffs reviewed before full rollout.
