---
id: computing-software.cybersecurity-defensive.trivy.select-and-skip-files-for-scanning
name: select-and-skip-files-for-scanning
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [skip-files, skip-dirs, file-patterns, doublestar, glob, analyzer, scan-scope]
level: practitioner
status: docs-checked
description: "Include or exclude files and directories in a Trivy scan with --skip-files, --skip-dirs and --file-patterns, including glob and regex syntax."
sources:
  - https://trivy.dev/latest/docs/guide/configuration/skipping/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy walks the target looking for known files (for example `/lib/apk/db/installed` or `requirements.txt`). These flags steer that, and differ from filtering results.

`--skip-files` and `--skip-dirs` apply to the vulnerability, misconfiguration, secret and license scanners. Glob patterns follow the doublestar library:
```bash
trivy image --skip-files "./testdata/*/bar" .
trivy config --skip-files "./foo/**/*.tf" .
trivy image --skip-dirs "./testdata/*" .
trivy config --skip-dirs "**/.terraform" .
```
The last pattern matches `./foo/.terraform` and `./foo/bar/.terraform` but not `./.terraform`. In the YAML config they live under `scan:` as `skip-files:` and `skip-dirs:`.

`--file-patterns` adds detection with the form `<analyzer>:<path>`, and does not disable default detection. The path may be a regular expression, and the flag can repeat:
```bash
trivy fs --file-patterns "pip:requirements-.*\.txt" .
trivy fs --scanners misconfig,vuln --file-patterns "dockerfile:.production.docker" --file-patterns "pip:.requirements-test.txt" .
```
It works for vulnerability and misconfiguration scanners, for the license scanner only with `--license-full`, but not for secret. It does not apply to parsers handling several extensions, such as Terraform's `.tf` and `.tf.json`.

## Checked

2026-11-03. Read and confirmed against the Selecting files for scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: the claim that skip-files and skip-dirs also cover the crypto scanner (the page's table lists only vulnerability, misconfiguration, secret and license for them).

Method: documentation only; no commands were run.
