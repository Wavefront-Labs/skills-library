---
id: computing-software.devops-ci-cd.tilt.tilt-snapshots
name: tilt-snapshots
category: computing-software
field: devops-ci-cd
product: tilt
tags: [snapshots, tilt, debugging, tilt-cli]
level: intro
status: docs-checked
description: "Save Tilt state to a snapshot file and view it later for async debugging or bug reports."
sources:
  - "https://docs.tilt.dev/snapshots.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt snapshots

Goal: capture your Tilt state in a file so you, or another Tilt user, can later load it and explore logs and error status for that moment. Useful for async debugging and for adding context to bug reports.

## From the command line

With a Tilt session running, create a JSON file:

```bash
tilt snapshot create <file>
```

View it:

```bash
tilt snapshot view <file>
```

A header at the top of the screen shows you are viewing a Snapshot.

## From the web UI

Click the snapshots icon at the top-right of the screen, then click the "Save Snapshot" button. To view the downloaded file, run `tilt snapshot view <file>` in a terminal.

## Deprecated: Tilt Cloud

Snapshots were once stored in Tilt Cloud, a hosted service. That is deprecated in favour of the file-based flow, which is described as more flexible and easier to understand. The linked blog post is at blog.tilt.dev/2022/05/12/offline-snapshots.html.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Sharing Snapshots page in full. Confirmed `tilt snapshot create` and `tilt snapshot view`, the header, the web UI Save Snapshot flow and the Tilt Cloud deprecation. Nothing removed. The skill is thin. 

Method: documentation only; no commands were run.
