---
id: computing-software.collaboration-platform-administration.zulip.logical-data-export
name: logical-data-export
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [data-export, manage-py-export, deactivate-flag, zulip-cloud-current]
level: practitioner
status: docs-checked
description: "Export a Zulip organization with manage.py export, deciding between stop-server and --deactivate, the zulip-cloud-current upgrade for Cloud imports, and downsides versus backups."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Logical data export

The export tool moves a Zulip organization between installations. It captures all non-transient data except secrets such as passwords and API keys. Use the backup tool instead when applicable, because exports have downsides: passwords are randomised and everyone is logged out of web and mobile; bots and integrations need new API keys; users, channels and messages are usually renumbered, breaking external links.

Before exporting, upgrade to the latest maintenance release. If the data is going to Zulip Cloud, first upgrade to the `zulip-cloud-current` branch with `upgrade-zulip-from-git zulip-cloud-current`, since Cloud runs pre-release code months ahead of the stable release.

Freeze changes first, using one of:

1. `./scripts/stop-server`, preferred on single-organization servers.
2. `--deactivate` on the export command, which deactivates the organization, ends all sessions and blocks logins and API access. Better when exporting one organization without disturbing others.

Run as the `zulip` user:

```
cd ~zulip/deployments/current
# ./scripts/stop-server
# export DEACTIVATE_FLAG="--deactivate"
./manage.py export -r '' $DEACTIVATE_FLAG
```

The `-r` option names the organization; an empty string is the one on the root domain. The result is a compressed archive such as `/tmp/zulip-export-<timestamp>-<random>.tar.gz` containing JSON files plus all the organization's uploaded files.

## Checked

Confirmed against the Data export section of the export-and-import page: what is and is not exported, the downsides versus backups, the zulip-cloud-current upgrade, the two ways to freeze changes, the export command and the archive contents. Removed the web UI and S3 download paragraph (not on this page).

Method: docs-checked 2026-11-09 against docs/production/export-and-import.md in the zulip/zulip repository (main), the source of the cited page.
