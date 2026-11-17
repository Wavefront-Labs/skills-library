---
id: computing-software.rpa-and-low-code.uipath.uipath-cli-pack-publish
name: uipath-cli-pack-publish
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-ci-cd-publish, uipath-cli-pack-publish]
level: advanced
status: draft
description: "Build packages in a pipeline."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Package and publish with the UiPath CLI
**Goal:** Build packages in a pipeline.

- The UiPath CLI (`uipcli package pack <project>` and `uipcli package deploy`) packs and deploys to Orchestrator (confirm syntax for your CLI version).
- Run Workflow Analyzer and tests in the pipeline.
- Use semantic versioning.

## Gotchas
- Authenticate with an external application, not a personal account.

## Self-check
Pipeline publishes a package visible in Orchestrator.
