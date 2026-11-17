---
id: computing-software.collaboration-platform-administration.zulip.compare-settings-after-upgrade
name: compare-settings-after-upgrade
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [compare-settings, prod-settings-template, settings-py-merge]
level: practitioner
status: docs-checked
description: "After a major Zulip upgrade, merge new settings.py documentation: compare-settings-to-template, prod_settings_template.py, backup, settings-new.py and restart."
sources: ["https://zulip.readthedocs.io/en/latest/production/upgrade.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Refreshing settings.py after an upgrade

`/etc/zulip/settings.py` is never modified by upgrades, so it is based on the template from whichever version first installed it. New settings and their documentation can therefore be missing. After upgrading across major versions, compare it with the current template at `~zulip/deployments/current/zproject/prod_settings_template.py`.

1. Back up and copy the template:

```
cp -a /etc/zulip/settings.py ~/zulip-settings-backup.py
cp -a ~zulip/deployments/current/zproject/prod_settings_template.py /etc/zulip/settings-new.py
```

2. Open both files. For each setting you have set in `settings.py`, find its section in `settings-new.py` and copy your value across.

A helper finds the most likely template version your file came from and shows your modifications:

```
~zulip/deployments/current/scripts/setup/compare-settings-to-template
```

If a setting of yours has no match in the new template, check the changelog; it may have been removed.

3. Overwrite and restart. This should change nothing, and it is far better to find out immediately if it does:

```
cp -a /etc/zulip/settings-new.py /etc/zulip/settings.py
su zulip -c '~zulip/deployments/current/scripts/restart-server'
```

Take the backup seriously, particularly if you lack a recent complete server backup.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/upgrade.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.
