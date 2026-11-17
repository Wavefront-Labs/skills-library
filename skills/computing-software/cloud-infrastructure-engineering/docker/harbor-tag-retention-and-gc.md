---
id: computing-software.cloud-infrastructure-engineering.docker.harbor-tag-retention-and-gc
name: harbor-tag-retention-and-gc
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, harbor, harbor-retention, garbage-collection, retention, image-lifecycle, tag-immutability]
level: advanced
status: docs-checked
description: "Keep Harbor storage under control: tag retention rules (by count, age, pull time), dry runs, immutability interplay, and scheduled garbage collection that actually frees space."
sources: ["https://goharbor.io/docs/main/working-with-projects/working-with-images/create-tag-retention-rules/", "https://goharbor.io/docs/main/administration/garbage-collection/", "https://goharbor.io/docs/main/working-with-projects/working-with-images/create-tag-immutability-rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Harbor tag retention and garbage collection

Retention **deletes tags/artifacts** per project. Garbage collection **frees blob storage**
system-wide. You need both: retention alone leaves the bytes on disk.

## Retention rules (Project > Policy > Tag Retention)
A rule selects repositories and tags, then keeps a subset. You can define up to 15 rules per project;
multiple rules combine with OR logic, rules run concurrently, and their retained sets are merged.
Retention is matched per tag but applied per artifact: if an artifact has several tags and only some
match, the artifact and all its tags are retained.

Typical policy:
| Repositories | Tags | Retain |
|---|---|---|
| `**` | `v*` (releases) | most recently pushed 20 artifacts |
| `**` | `main-*` | pushed within the last 30 days |
| `**` | `pr-*` | most recently pushed 5 |
| `**` | `**` | pulled within the last 90 days (safety net for anything in use) |

Options: "retain the most recently pushed # artifacts", "retain the most recently pulled #
artifacts", "retain the artifacts pushed within the last # days", "retain the artifacts pulled within
the last # days", "retain always"; repositories and tags are each set to matching or excluding with
wildcards (`*`, `**` per doublestar), plus an "untagged artifacts" checkbox.
Always **Dry Run** first: a rule cannot be reverted once run. One schedule applies to all rules
(hourly, daily, weekly or custom cron).

## Interplay
- Tag immutability rules also stop an immutable tag being deleted, and the artifact holding it; other
  tags on the same digest can still be deleted. Immutability rules use OR logic.
- Project quotas (maximum storage or tag count, set by the system administrator) are a separate control.

## Garbage collection (Administration > Clean Up)
- Run GC after retention, e.g. weekly. Harbor runs GC without interrupting push, pull or delete, and
  skips blobs and manifests with a timestamp inside a 2 hour window to protect uploads in progress.
  GC Now can be used only once per minute.
- Check "Allow garbage collection on untagged artifacts" to also delete untagged artifacts.
- Choose the number of parallel workers, schedule (none, hourly, daily at midnight, weekly at midnight
  Saturday, custom cron) and review the GC history; Dry Run prints the blobs eligible for deletion and a
  rough estimate of space to be freed.

## Verify
- Quota and storage usage reflect freed space after GC runs.
- Retention execution log: number of retained vs deleted per repository.
- Object storage/bucket size trend over a few weeks.

## Gotchas
- Kubernetes nodes running a pod with a tag deleted by retention keep working until the pod
  is rescheduled to a node without the image: then `ImagePullBackOff`. The "pulled within"
  safety-net rule exists for this.
- Proxy cache projects need retention too or they grow unbounded.

## Checked

2026-10-26. Documentation release: Harbor website docs main (goharbor/website, last commit 2026-10-15): create-tag-retention-rules, create-tag-immutability-rules, garbage-collection. Confirmed: 15 rule limit, OR logic and concurrent evaluation, per-artifact retention of all tags, the five retain options, matching/excluding filters, dry run warning and single schedule for all rules, immutability behaviour on tag deletion, GC page (workers, untagged option, dry run, GC Now, schedules, 2 hour window, once per minute). Removed unconfirmed claims: index children and signature/SBOM deletion semantics, immutability protecting from retention specifically, and a project-summary quota claim.

Method: documentation only; no commands were run.
