---
id: computing-software.systems-network-administration.cisco-networking.pyats-learn-and-diff
name: pyats-learn-and-diff
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [network-automation, pyats, genie, genie-parser, testbed, pre-post-change, network-testing]
level: practitioner
status: draft
description: "Use pyATS and Genie for pre/post change validation: testbed YAML, genie learn of features, genie diff of snapshots, parsed show output in Python, and simple pass/fail checks."
sources:
  - https://developer.cisco.com/docs/pyats/
  - https://pubhub.devnetcloud.com/media/genie-docs/docs/cookbooks/genie.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# pyATS learn and diff

pyATS connects to devices, Genie parses hundreds of show commands into structured data and models
whole features (OSPF, BGP, interfaces) across platforms. The killer use: snapshot before a change,
snapshot after, diff.

## Install and testbed
```
pip install "pyats[full]"
```
`testbed.yaml`:
```yaml
testbed:
  credentials:
    default: {username: "%ENV{NET_USER}", password: "%ENV{NET_PASS}"}
devices:
  core1:
    os: iosxe
    type: router
    connections:
      cli: {protocol: ssh, ip: 10.0.0.1}
  dist1:
    os: iosxe
    connections:
      cli: {protocol: ssh, ip: 10.0.0.2}
```

## Pre/post snapshot and diff
```
genie learn ospf bgp interface routing --testbed-file testbed.yaml --output pre/
# ... make the change ...
genie learn ospf bgp interface routing --testbed-file testbed.yaml --output post/
genie diff pre/ post/
```
The diff lists exactly what changed per device and feature (neighbour lost, route count changed,
interface down). Exclude noisy keys (counters, uptimes) with `--exclude`.

## Parsed output in Python
```python
from genie.testbed import load
tb = load("testbed.yaml")
dev = tb.devices["core1"]
dev.connect(log_stdout=False)
ospf = dev.parse("show ip ospf neighbor")
for intf, data in ospf["interfaces"].items():
    for nbr, n in data["neighbors"].items():
        assert n["state"].startswith("FULL"), f"{nbr} on {intf} is {n['state']}"
```
`genie parse "show version" --testbed-file testbed.yaml --devices core1` does the same from the
shell and prints JSON.

## Gotchas
- Parsers exist per OS and command; unsupported commands raise `SchemaEmptyParserError` or
  "parser not found": check the parser list on the Genie docs site.
- Learning full features on large routers takes time; learn only what the change touches.
- Keep snapshots with the change ticket as evidence.

## Verify
- [ ] `genie diff` after a no-op change shows no differences except excluded counters.
