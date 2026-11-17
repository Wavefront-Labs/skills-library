---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.reuse-licensing-metadata
name: reuse-licensing-metadata
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [reuse-licensing-metadata, reuse-specification, reuse, fsfe, licenses directory, dep5, reuse.toml, spdx header, license sidecar, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Apply REUSE: SPDX headers, LICENSES directory with texts and .license sidecars or REUSE.toml for non-commentable files."
sources:
  - https://reuse.software/spec-3.3/
  - https://reuse.software/tutorial/
  - https://reuse.software/dev/
  - https://github.com/fsfe/reuse-tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REUSE licensing metadata in a repository

Goal: every file carries clear copyright and licence information in a machine-readable way.

Rules (REUSE Specification 3.3):
- Each file has SPDX-FileCopyrightText and SPDX-License-Identifier tags in a comment, or a sidecar file name.ext.license, or an entry in REUSE.toml (the older .reuse/dep5 is deprecated).
- A LICENSES/ directory contains the full text of each licence used, each file named after its SPDX licence identifier plus a file extension (e.g. MIT.txt).
- Commands: reuse annotate --license MIT --copyright "Name" file; reuse download MIT; reuse lint; reuse spdx > sbom.spdx.

Method: add reuse lint to CI and pre-commit.

Gotchas:
- Binary files and images need sidecar or REUSE.toml.
- Use valid SPDX IDs or LicenseRef- with a text file.

Verify: reuse lint reports that the project is compliant.

## Checked

2026-11-02. Checked against the REUSE 3.3 specification (comment header tags, .license sidecar, REUSE.toml, DEP5 deprecated, LICENSES/ naming, LicenseRef), the REUSE tutorial (reuse annotate --license --copyright, reuse download, reuse lint, compliance message) and the reuse-tool man pages (reuse spdx writes to STDOUT). Fixed: the LICENSES/ file naming and the lint output wording.

Method: documentation only; no commands were run.
