---
id: computing-software.cloud-infrastructure-engineering.harbor.replication-rules
name: replication-rules
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [replication-rule, push-based, pull-based, flattening, harbor]
level: practitioner
status: docs-checked
description: "Create Harbor replication rules: push or pull, name and tag filter patterns, destination flattening, trigger modes, bandwidth, override and chunk copy."
sources:
  - https://goharbor.io/docs/main/administration/configuring-replication/create-replication-rules/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a rule under Administration, Replications, **New Replication Rule**, after an endpoint exists. Choose **Push-based** (to a Destination Registry) or **Pull-based** (from a Source Registry). You cannot replicate from Harbor v1.x to v2.0 or later.

Source resource filter: Name, Tag, Label (tag and label support matching or excluding) and Resource (images, artifacts or all). Name and tag patterns: `*` matches non-separator characters (not `/`), `**` matches including `/` and must be a whole path component, `?` one non-separator character, `{alt1,alt2}` alternatives. `library/*` matches `library/hello-world` but not `library/my/hello-world`; `library/**` matches both. Add `library` to replicate Docker Hub official images.

Destination Namespace: empty keeps the source namespace. Flattening for `a/b/c/d/img` into `namespace`: Flatten All Levels gives `namespace/img`, No Flattening keeps `a/b/c/d/img`, 1 level gives `namespace/b/c/d/img` (the default selection), 2 levels `namespace/c/d/img`, 3 levels `namespace/d/img`. Rules created before v2.3.0 default to Flatten All Levels.

Trigger mode: Manual and Scheduled (cron) do not replicate deletions. Event Based replicates push, retag and delete immediately; tick **Delete remote resources when locally deleted** to propagate deletes. Changing a label does not trigger replication.

Options: bandwidth per task in KB/s (`-1` unlimited; default 10 concurrent executions per jobservice pod); **Override**; **Copy by chunk** (Harbor to Harbor, chunk 10MB, change with `REPLICATION_CHUNK_SIZE=10485760` on jobservice); **Single active replication** skips runs while one is active. Very low bandwidth makes stopping a job slow (issue 15708).

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Creating a Replication Rule.
Method: documentation only; no commands were run.
