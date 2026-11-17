---
id: computing-software.cloud-infrastructure-engineering.podman.system-prune-cleanup
name: system-prune-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [system-prune, cleanup, dangling-images, volumes, build-containers, external, filter]
level: practitioner
status: docs-checked
description: "Reclaim space with podman system prune: what the default removes, --all, --volumes, --build safety, --external for transient storage, label and until filters."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-system-prune.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove unused resources deliberately.

`podman system prune [options]` removes unused containers (dangling and unreferenced), build containers, pods, networks and optionally volumes. The default prompt lists: all stopped containers, all networks not used by at least one container, all dangling images and all dangling build cache.

Flags: `--all`/`-a` recursively removes unused pods, containers, images, networks and volume data (maximum 50 iterations); unused images are dangling images plus any with no container based on them. `--volumes` also prunes volumes unused by any container; volumes are kept by default so important data is not deleted when no container currently uses them. `--build` removes build containers left by unexpectedly terminated builds; the page warns this is not safe and can interfere with builds in progress. `--force`/`-f` skips confirmation.

`--external` cleans remainders of previous containers or layers not referenced in the storage JSON files, which happen after unclean shutdowns or restarts in transient storage mode. In that mode the Podman database does not persist, so writable layers stay on disk after reboot; the page recommends running `podman system prune --external` during boot. It is incompatible with `--all` and `--filter`, and drops the default behaviour.

Filters (repeatable): `label=key` or `label=key=value` (and `label!=` forms for without), and `until=` taking Unix timestamps, date timestamps or Go durations such as `10m` or `1h30m`. Example: `podman system prune --filter label=role=cleanup`.

## Checked
2026-11-09: read the podman-system-prune man page in full and confirmed the default prompt list, --all (50 iterations), --volumes, --build warning, --external and its incompatibilities, --force, and the label and until filters. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.

