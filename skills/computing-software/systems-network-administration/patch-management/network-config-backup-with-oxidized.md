---
id: computing-software.systems-network-administration.patch-management.network-config-backup-with-oxidized
name: network-config-backup-with-oxidized
category: computing-software
field: systems-network-administration
product: patch-management
tags: [oxidized, network-config-backup, rancid, config-versioning, network-device-patching, patch-management]
level: practitioner
status: docs-checked
description: "Back up network device configs before upgrades with Oxidized: inventory sources, models, Git output, on-demand fetch via API before a change, and diffing after."
sources:
  - https://github.com/ytti/oxidized
  - https://github.com/ytti/oxidized/blob/master/docs/Configuration.md
  - https://github.com/ytti/oxidized-web
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network config backup before upgrade with Oxidized

Oxidized (a RANCID replacement) pulls configs from routers, switches and firewalls on a schedule and commits each change to Git. Before an upgrade you force a fresh fetch, and after you diff.

## Minimal config (`~/.config/oxidized/config`, merged over `/etc/oxidized/config`)
```yaml
username: backup
password: <from-vault-or-env>
model: ios
interval: 3600
use_syslog: false
rest: 127.0.0.1:8888
input:
  default: ssh
  ssh:
    secure: true
output:
  default: git
  git:
    user: Oxidized
    email: oxidized@example.com
    repo: "/var/lib/oxidized/configs.git"
source:
  default: csv
  csv:
    file: "/etc/oxidized/router.db"
    delimiter: !ruby/regexp /:/
    map: {name: 0, model: 1, group: 2}
```
`router.db`: `core-sw1.example.com:ios:core`, `fw1.example.com:fortios:edge`, `spine1:nxos:dc`. The CSV source reads a RANCID-compatible `router.db`; SQLite, MySQL and HTTP sources also exist. See the project's model list for the model name of each device type.

## Force a backup right before the change
```sh
curl -s http://127.0.0.1:8888/node/next/core-sw1.example.com     # queue immediate fetch
sleep 30
curl -s http://127.0.0.1:8888/node/fetch/core-sw1.example.com    # print latest stored config
git -C /var/lib/oxidized/configs.git log --oneline -3
```

## After upgrade
Trigger another fetch and diff the last two commits with `git -C /var/lib/oxidized/configs.git diff HEAD~1`. Expect version banners and new default lines; investigate missing interface, ACL or routing lines.

## Gotchas
- Store credentials outside the config (env vars / vault) and restrict the Git repo; configs contain secrets (hashes, SNMP communities, PSKs).
- A device failing login stays at its last good backup silently; alert on failed node status.

## Verify
Pre-change fetch timestamp is within minutes of the change start; post-change diff reviewed and attached to the change record.

## Checked
2026-10-28. Confirmed against the Oxidized README and Configuration.md (config locations and merge order, `interval` in seconds, REST `/node/next/[NODE]` and `/node/fetch/[NODE]`, CSV source and `router.db` compatibility, `delimiter`/`map`, git output, `use_syslog`, RANCID replacement). Removed: the per-device model list, NetBox as a named source, the claim that models strip volatile lines, the `no_connection` status name and per-group git paths, none of which the pages state.
Method: documentation only; no commands were run.
