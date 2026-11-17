---
id: computing-software.cloud-infrastructure-engineering.saltstack.requisites-onchanges-onfail
name: requisites-onchanges-onfail
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, requisites, onchanges, onfail, failhard, states]
level: practitioner
status: docs-checked
description: "Run Salt states only when another state changed (onchanges) or failed (onfail): multi-target logic, the _in reversal trap and the failhard interaction."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/requisites.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Requisites: onchanges and onfail

**onchanges** (since 2014.7.0): run this state only if a target succeeded with changes. With several targets it runs if any changed. No effect on SLS-level targets.

```yaml
myservice:
  file.managed:
    - name: /etc/myservice/myservice.conf
    - source: salt://myservice/files/myservice.conf
  cmd.run:
    - name: /usr/local/sbin/run-build
    - onchanges:
      - file: /etc/myservice/myservice.conf
```

Trap: writing `onchanges_in` where `onchanges` is meant reverses the logic. The `cmd.run` then always runs, and the file only changes if the command reports changes.

**onfail** (since 2014.7.0): run only when a target fails. Several targets use OR logic since 2016.11.0 (earlier releases used AND).

```yaml
backup_mount:
  mount.mounted:
    - name: /mnt/share
    - device: 192.168.40.34:/share
    - fstype: nfs
    - onfail:
      - mount: primary_mount
```

Variants:
- `onchanges_any` and `onfail_any`: fire if any target changed or failed.
- `onfail_all` (Neon): fire only if every target failed.

Caveat: if `failhard` is `True` globally or in the state, `onfail`, `onfail_in` and `onfail_any` are ignored. Set `failhard: False` on the state that might fail.

## Checked

2026-11-04: read the Salt requisites reference page in full. Confirmed onchanges (2014.7.0) and the onchanges_in trap, onfail (2014.7.0), OR logic from 2016.11.0, onfail_all from Neon, the _any forms and the failhard note. Nothing removed.

Method: documentation only; no commands were run.

