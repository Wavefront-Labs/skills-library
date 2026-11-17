---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-tools-bucket
name: thanos-tools-bucket
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thanos, thanos-tools-bucket, bucket-verify, bucket-rewrite, bucket-inspect, bucket-mark, bucket-web, series-deletion]
level: advanced
status: docs-checked
description: "Maintain a Thanos bucket with thanos tools bucket: ls, inspect, web UI, verify/repair, mark for deletion or no-compact, rewrite to delete series, and replicate."
sources: ["https://thanos.io/tip/components/tools.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# thanos tools bucket

All commands take `--objstore.config-file=objstore.yml`.

| Command | Use |
|---|---|
| `bucket ls -o wide` | list blocks with time range and labels |
| `bucket inspect --selector='cluster="prod"' --sort-by=FROM` | table of blocks, sortable (`--sort-by=FROM`) and filterable by external labels (`--selector`) |
| `bucket web --http-address=:8080` | interactive web UI to inspect bucket blocks |
| `bucket verify --issues=overlapped_blocks --issues=index_known_issues` | find problems; `overlapped_blocks` is verify-only, while `index_known_issues` and `duplicated_compaction` can be repaired with `--repair --objstore-backup.config-file=backup.yml`. Disable the compactor first |
| `bucket mark --id=<ULID> --marker=deletion-mark.json --details="corrupt"` | compactor deletes after `--delete-delay` |
| `bucket mark --id=<ULID> --marker=no-compact-mark.json` | exclude a block from compaction (e.g. huge or problematic) |
| `bucket rewrite --id=<ULID> --rewrite.to-delete-config-file=del.yml --no-dry-run` | rewrite a block without matching series |
| `bucket replicate --objstore-to.config-file=dr.yml` | copy blocks to another bucket (DR) |
| `bucket cleanup` | delete blocks marked for deletion now |
| `bucket downsample` | run downsampling manually |
| `bucket upload-blocks --path=./blocks` | upload backfilled blocks (newer versions) |

## Deleting series (e.g. leaked PII)
```yaml
# del.yml
- matchers: '{__name__="http_requests_total", user_email=~".+"}'
```
```bash
for id in <ULIDs of the blocks that hold the series, from `bucket ls`>; do
  thanos tools bucket rewrite --id=$id --rewrite.to-delete-config-file=del.yml --delete-blocks --no-dry-run
done
```
Rewrite creates a new block and (with `--delete-blocks`) marks the old one for deletion. Run with the
compactor stopped or on blocks it is not touching.

## Gotchas
- Always dry-run (`rewrite` is dry-run by default; `verify` without `--repair` is read-only).
- Store gateways re-sync blocks on an interval (`--sync-block-duration`, default 15m), so deleted or rewritten blocks leave queries only after the next sync.

## Verify
- [ ] `bucket verify` reports no issues after maintenance.
- [ ] Queries for deleted series return empty for all time ranges.

## Checked
- 2026-10-28. Confirmed against the Thanos Tools page (subcommands `ls`, `inspect`, `web`, `verify`, `mark`, `rewrite`, `replicate`, `cleanup`, `downsample`, `upload-blocks`; flags `-o wide`, `--selector`, `--sort-by`, `--issues`, `--repair`, `--objstore-backup.config-file`, `--marker`, `--details`, `--rewrite.to-delete-config-file`, `--no-dry-run`, `--[no-]delete-blocks`, `--objstore-to.config-file`), the Compact page (`deletion-mark.json`), the Storage page (`no-compact-mark.json`) and the Store page (`--sync-block-duration=15m`).
- Removed: the column list for `inspect`, the `jq .ulid` field name and the "same as compactor/store UI" remark.
Method: documentation only; no commands were run.
