---
id: computing-software.cloud-infrastructure-engineering.ansible.saving-and-rolling-back-network-configs
name: saving-and-rolling-back-network-configs
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, network-automation, save-when, network-rollback, config-backup]
level: practitioner
status: docs-checked
description: "Persist running config to startup with save_when, and roll back network changes with config replace, archives, commit confirmed and backup restores."
sources: ["https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_config.py", "https://github.com/ansible-collections/junipernetworks.junos/blob/main/plugins/modules/junos_config.py", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/modules/cli_config.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Saving and rolling back network configs

## save_when (IOS-style platforms)
```yaml
- name: Apply NTP config and save only if changed
  cisco.ios.ios_config:
    lines:
      - ntp server 10.0.0.1
      - ntp server 10.0.0.2
    save_when: modified
```
| save_when | Behaviour |
|---|---|
| `never` (default) | running config only; lost on reload |
| `modified` | `copy run start` if running differs from startup after the task |
| `changed` | save if this task changed something |
| `always` | always copy running to startup; the module always reports changed |

Resource modules (`ios_vlans`, `ios_interfaces`) do not save: add a final `ios_config: save_when: modified` task.

## Rollback strategies
1. **Backup then restore**
```yaml
- cisco.ios.ios_config:
    backup: true
    backup_options: {dir_path: backups/, filename: "{{ inventory_hostname }}.cfg"}
```
Restoring a backup to the device (for example with the platform's config replace command) is a vendor feature: check the vendor documentation.

2. **Commit confirmed** (Junos)
```yaml
- junipernetworks.junos.junos_config:
    src: candidate.conf
    confirm: 5           # auto-rollback after 5 minutes unless confirmed
- junipernetworks.junos.junos_config:
    confirm_commit: true # confirm once health checks pass
```
`junos_config` also takes `rollback: <id>` to return to a stored rollback configuration; `0` is the most recent commit.

3. **Replace with full intended config** (`replace: config` / `state: replaced|overridden`) from a known-good template.

## Gotchas
- Without `save_when`, a reload after an outage reverts changes and drift appears "randomly".
- `save_when: modified` saves whenever running differs from startup, so pre-existing unsaved changes get saved too.
- Test rollback paths in a lab before relying on them.

## Verify
- [ ] A `cisco.ios.ios_config` task with `diff_against: startup` and `check_mode: true` reports no difference.

## Checked

Checked 2026-10-26 against the cisco.ios `ios_config` and junipernetworks.junos `junos_config` module sources (main). Confirmed: `save_when` choices always, never (default), modified and changed with the semantics in the table; `junos_config` `confirm` (minutes), `confirm_commit` and `rollback` (identifier, 0 is the most recent commit). Removed the IOS `configure replace` command, the claim that IOS-XR and EOS use the same commit-confirmed options, and the archive-feature remark, none of which those module pages state.

Method: documentation only; no commands were run.
