---
id: computing-software.collaboration-platform-administration.nextcloud.file-version-retention-pattern
name: file-version-retention-pattern
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [files-versions, versions-retention-obligation, expiry, quota, config-php]
level: practitioner
status: docs-checked
description: "Understand the default Nextcloud version thinning pattern, the 50 percent free space cap, and set versions_retention_obligation values."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/file_versioning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control how long old file versions live.

The Versions app (`files_versions`) expires old versions so users stay within quota. Default thinning pattern:
- first second: one version
- first 10 seconds: one every 2 seconds
- first minute: one every 10 seconds
- first hour: one every minute
- first 24 hours: one every hour
- first 30 days: one every day
- after 30 days: one every week

Versions are adjusted each time a new one is created, and the latest in each time window is always kept.

Space cap: the Versions app never uses more than 50% of the user's currently available free space. Beyond that, the oldest versions go first. When space is low Nextcloud sorts versions oldest to newest and removes the oldest, while preserving the most recent ones. A background job also cleans up each user's old or orphaned versions. Versions a user has named are never deleted.

Setting, in `config.php`:

```
'versions_retention_obligation' => 'auto',
```

Values:
- `auto` is the default pattern
- `D, auto`: keep at least D days, apply the rules after that
- `auto, D`: delete anything older than D days, apply the rules to the rest
- `D1, D2`: keep at least D1 days and delete after D2 days
- `disabled`: versions are still created but never pruned automatically

Check: after changing the value, wait for the background job and compare a test file's version list against the new rule.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/file_versioning.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
