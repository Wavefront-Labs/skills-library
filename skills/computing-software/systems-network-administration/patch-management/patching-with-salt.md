---
id: computing-software.systems-network-administration.patch-management.patching-with-salt
name: patching-with-salt
category: computing-software
field: systems-network-administration
product: patch-management
tags: [salt-patching, saltstack, salt, pkg-uptodate, patch-deployment, patch-management]
level: practitioner
status: docs-checked
description: "Patch Linux and Windows fleets with Salt: targeting, pkg.upgrade and pkg.uptodate states, batch mode, reboots, orchestration and return data for reporting."
sources:
  - https://docs.saltproject.io/en/latest/ref/modules/all/salt.modules.yumpkg.html
  - https://docs.saltproject.io/en/latest/ref/states/all/salt.states.pkg.html
  - https://docs.saltproject.io/en/latest/topics/targeting/batch.html
  - https://docs.saltproject.io/en/latest/ref/modules/all/salt.modules.win_wua.html
  - https://docs.saltproject.io/en/latest/ref/states/all/salt.states.saltmod.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patching with Salt

## Ad hoc
```sh
salt -G 'os_family:RedHat' pkg.list_upgrades
salt -C 'G@role:web and G@env:prod' pkg.upgrade --batch-size 10%
salt 'db*' pkg.upgrade refresh=True                    # all packages
salt '*' cmd.run 'dnf -y update --security' --batch 5   # security only on EL
salt -G 'os:Windows' win_wua.list install=True categories='["Security Updates","Critical Updates"]'
```
`--batch-size` (`-b`) runs N or N% minions at a time; `--batch-wait` adds pause between batches.

## State (repeatable, reportable)
```yaml
# /srv/salt/patch/init.sls
patch-all:
  pkg.uptodate:
    - refresh: True
reboot-if-needed:
  module.run:
    - system.reboot:
      - at_time: 1
    - onlyif: test -f /var/run/reboot-required     # Debian/Ubuntu
# EL: replace onlyif with  - unless: dnf needs-restarting -r   (exit 1 means reboot needed)
```
`salt -N web-prod state.apply patch --batch 2 test=True` first, then without `test=True`.

## Orchestration (dependent order)
```yaml
# /srv/salt/orch/patch_app.sls
drain_lb:
  salt.state: {tgt: 'lb*', sls: lb.drain_web}
patch_web:
  salt.state: {tgt: 'web*', sls: patch, batch: 1, require: [{salt: drain_lb}]}
```
Run `salt-run state.orchestrate orch.patch_app`.

## Reporting
Use a returner (`--return <returner>`) or the job cache: `salt-run jobs.lookup_jid <jid>`; `salt '*' pkg.version openssl --out=json` for verification.

## Gotchas
- `pkg.uptodate` with no `pkgs` upgrades everything; restrict with `pkgs:` or use holds (`pkg.hold`).
- Minions that are offline are simply skipped; check `salt-run manage.down` before declaring success.
- Kernel updates need the reboot step; Salt does not reboot by itself.

## Verify
`salt '*' pkg.list_upgrades` returns empty for patched targets; job return shows no failures; reboot-required check is false.

## Checked
Date: 2026-10-27. Documentation checked: Salt batch page (`-b`/`--batch-size`, `--batch-wait`), `salt.modules.yumpkg` (`pkg.list_upgrades`, `pkg.upgrade` with `refresh`), `salt.states.pkg` (`uptodate` with `refresh` and `pkgs`, `held`), `salt.modules.win_wua` (`list` with `install` and `categories`), `salt.modules.system` (`reboot` with `at_time` in minutes), `salt.runners.manage` (`down`), `salt.runners.jobs` (`lookup_jid`), `salt.runners.state` (orchestrate), `salt.states.saltmod` (`batch`), nodegroups page (`-N`), dnf-plugins-core needs-restarting (`-r` exit 1 means reboot needed). Replaced the unconfirmed `mysql`/`smtp` returner names with a placeholder and used `dnf needs-restarting -r`.

Method: documentation only; no commands were run.
