---
id: computing-software.digital-forensics-incident-response.log-analysis.writing-custom-velociraptor-artifacts
name: writing-custom-velociraptor-artifacts
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [velociraptor-artifacts, velociraptor, vql, artifact-development, threat-hunting, dfir]
level: advanced
status: draft
description: "Write custom Velociraptor artifacts in YAML: parameters, sources, preconditions, tool dependencies, column types, and reporting, and test them before fleet-wide hunts."
sources: ["https://docs.velociraptor.app/docs/vql/artifacts/", "https://docs.velociraptor.app/exchange/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing custom Velociraptor artifacts

**Goal:** package incident-specific VQL into a reusable, parameterised artifact that others
can run as collections or hunts.

## Skeleton
```yaml
name: Custom.Windows.IR014.SuspiciousServices
description: |
  Services whose ImagePath points to user-writable paths (IR-014 TTP).
author: IR team
type: CLIENT
precondition: SELECT OS FROM info() WHERE OS = 'windows'
parameters:
  - name: PathRegex
    default: '(?i)\\\\(users|programdata|windows\\\\temp)\\\\'
    type: regex
  - name: AlsoHash
    type: bool
sources:
  - query: |
      LET svcs = SELECT Key.Name AS Service, ImagePath,
             expand(path=ImagePath) AS Exe
        FROM read_reg_key(globs='HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\*')
        WHERE ImagePath =~ PathRegex
      SELECT Service, ImagePath,
             if(condition=AlsoHash, then=hash(path=Exe).SHA256) AS SHA256
      FROM svcs
column_types:
  - name: SHA256
    type: hash
```
Other keys: `tools:` (declare external binaries such as a scanner, served by the server and
verified by hash), `reports:` (templated output), `export:`/`imports:` for shared VQL,
multiple `sources` with names, `type: SERVER` or `CLIENT_EVENT` for monitoring artifacts.

## Workflow
1. Develop the VQL in a notebook on a test client.
2. Add artifact in GUI (View Artifacts -> Add) or `velociraptor artifacts` with
   `--definitions` directory; it syntax-checks on save.
3. Collect on one client with a positive control; check performance.
4. Hunt. Version the YAML in git with the case or team repo; share good ones to the
   Artifact Exchange.

## Gotchas
- Parameter types matter (`regex`, `bool`, `int`, `csv`, `yara`); wrong types silently
  coerce strings.
- Name custom artifacts with a prefix (`Custom.`) to avoid clashing with built-ins on upgrade.

## Verify
`velociraptor artifacts verify` (or GUI save) passes, and the artifact returns the planted
artefact on the control host and nothing on a clean host.
