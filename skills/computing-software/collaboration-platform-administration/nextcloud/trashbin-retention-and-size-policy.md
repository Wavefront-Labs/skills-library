---
id: computing-software.collaboration-platform-administration.nextcloud.trashbin-retention-and-size-policy
name: trashbin-retention-and-size-policy
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [files-trashbin, trashbin-retention-obligation, deleted-files, quota, occ-trashbin]
level: practitioner
status: docs-checked
description: "Set trashbin_retention_obligation, understand the 30 day minimum and 50 percent of remaining quota default, and which items get purged first."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/trashbin_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict when deleted files are permanently removed.

The `files_trashbin` app (Deleted files) moves deleted items to the trash. Items are permanently deleted when the owner chooses *Delete permanently*, when the retention policy expires them, or when the effective size limit is exceeded and the item is eligible. The app also supplies the commands `trashbin:size`, `trashbin:expire`, `trashbin:cleanup` and `trashbin:restore`.


Default policy `auto`: items are kept at least 30 days, and after that may be deleted when space is needed.

Default size limit:
- account with a quota: up to 50% of the account's remaining quota (not total). A 10 GB quota with 8 GB used gives an allowance based on 2 GB.
- no quota: available filesystem space
- an explicit global or per-account size overrides the default

When over the limit, the oldest items are processed first, but only eligible ones.

Setting, in `config/config.php`:

```
'trashbin_retention_obligation' => 'auto',
```

Values (D1 and D2 are days): `auto` (same as `auto, auto`); `D1, auto` keeps at least D1 days; `auto, D2` allows deletion when space is needed and always deletes items older than D2 days; `D1, D2` keeps at least D1 days and deletes after D2.

Check: `occ trashbin:size` for a user reflects your policy after expiry runs.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/trashbin_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
