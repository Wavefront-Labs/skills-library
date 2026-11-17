---
id: computing-software.collaboration-platform-administration.vikunja.cli-repair-commands
name: cli-repair-commands
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, repair-dry-run, orphan-projects, task-positions, file-mime-types]
level: advanced
status: docs-checked
description: "Use vikunja repair subcommands to fix orphaned projects, duplicate task positions, orphan position rows and missing file MIME types, previewing with --dry-run."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/integrations/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vikunja repair <sub>` fixes data integrity problems. Every subcommand accepts `--dry-run` to preview.

- `repair projects`: re-parents projects whose parent no longer exists to the top level. Symptom: a project that cannot be un-archived, modified or deleted because permission checks fail up the broken parent chain (seen after e.g. Trello imports).
- `repair task-positions`: finds views with duplicate task positions (race conditions, old bugs) that make tasks jump around on refresh. It redistributes conflicting tasks locally, falling back to recalculating the whole view.
- `repair orphan-positions`: deletes position rows pointing at tasks or views that no longer exist.
- `repair file-mime-types`: fills in the MIME type for files with an empty or NULL mime column, detected from stored content. Relevant after upgrading from a version that did not store MIME types.

In Docker, run the command in the container: `docker exec <container> /app/vikunja/vikunja repair projects --dry-run`.

## Checked

2026-11-04: checked against the CLI page (repair section). Removed the "back up" advice, which the page does not give.

Method: documentation only; no commands were run.
