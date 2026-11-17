---
id: computing-software.messaging-and-integration.redpanda.rpk-group-list-and-describe-lag
name: rpk-group-list-and-describe-lag
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rpk, rpk-group, consumer-groups, lag, group-state, coordinator]
level: practitioner
status: docs-checked
description: "List consumer groups by state and describe group lag with rpk group list and rpk group describe, including regex matching, summary and per-topic lag views."
sources:
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-group/rpk-group-list/
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-group/rpk-group-describe/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**List groups.** `rpk group list` (alias `rpk group ls`) shows every group known to Redpanda, including empty groups that have not yet expired. The BROKER column is the group's coordinator, useful for tracking down unknown groups. Filter with `-s, --states`, using any of:
- `PreparingRebalance`: preparing to rebalance.
- `CompletingRebalance`: waiting on the leader for assignments.
- `Stable`: not empty and no membership changes in progress.
- `Dead`: transient, group being removed.
- `Empty`: no members.

Output format is chosen with `--format` (json, yaml, text, wide; new in v26.2.1 for this command).

```bash
rpk group list [flags]
```

**Describe groups.** `rpk group describe` shows members, calculates lag and prints details. COORDINATOR-PARTITION is the `__consumer_offsets` partition responsible for the group, if known.

```bash
rpk group describe <foo> <bar>
rpk group describe -r '^f.*' '.*r$'
rpk group describe -r '*'
rpk group describe -r .
```
`-r, --regex` treats arguments as regular expressions and describes any group matching any of them.

Flags to narrow output: `-s, --print-summary` (summary only), `-c, --print-commits` (commits section only), `-t, --print-lag-per-topic` (aggregated lag per topic), `-i, --instance-ID` (member instance IDs) and `--format`.

## Checked

2026-11-04. States, aliases, examples and flags were confirmed on the two rpk group pages.

Method: documentation only; no commands were run.
