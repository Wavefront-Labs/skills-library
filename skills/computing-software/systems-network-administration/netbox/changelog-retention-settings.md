---
id: computing-software.systems-network-administration.netbox.changelog-retention-settings
name: changelog-retention-settings
category: computing-software
field: systems-network-administration
product: netbox
tags: [changelog-retention, changelog-skip-empty, enforce-global-unique]
level: practitioner
status: docs-checked
description: "Control how long changes are kept and how global uniqueness is enforced."
sources: ["https://netboxlabs.com/docs/netbox/configuration/miscellaneous/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Change log and miscellaneous settings

Goal: keep history manageable and avoid surprises.

**Change log**

- `CHANGELOG_RETENTION` default 90 days. `0` keeps changes indefinitely; if you do, periodically delete old entries or the database may fill.
- `CHANGELOG_RETAIN_CREATE_LAST_UPDATE` (default False): when pruning, keep each non-deleted object's original create record and its most recent update record. Objects with a delete record are pruned normally.
- `CHANGELOG_SKIP_EMPTY_CHANGES` (default True): no record when an update changes no field values. `last_updated` still reflects the update.

**Uniqueness.** `ENFORCE_GLOBAL_UNIQUE` (default True) prevents duplicate prefixes and IP addresses in the global table, meaning those not assigned to a VRF. Set False to allow duplicates.

**Other**

- `ADMINS`: list of name and email pairs notified of critical errors.
- `BANNER_TOP`, `BANNER_BOTTOM`, `BANNER_LOGIN`, `BANNER_MAINTENANCE`: banner content; HTML is allowed on login and maintenance banners.
- `DATA_UPLOAD_MAX_MEMORY_SIZE`: 2,621,440 bytes (2.5 MB).
- `STREAMING_EXPORTS` (default False): stream CSV bulk exports to cut memory use; it is opt-in because there is no Content-Length header and errors surface after the response starts.
- `CENSUS_REPORTING_ENABLED` default True.

**Checklist**

1. Pick a retention window.
2. Decide on global uniqueness.
3. Enable streaming for large exports.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Miscellaneous settings page: CHANGELOG_RETENTION default 90 and 0 keeps indefinitely, CHANGELOG_RETAIN_CREATE_LAST_UPDATE, DATA_UPLOAD_MAX_MEMORY_SIZE default 2621440 (2.5 MB), STREAMING_EXPORTS, CENSUS_REPORTING_ENABLED, banner parameters. Removed: Nothing.

Method: documentation only; no commands were run.
