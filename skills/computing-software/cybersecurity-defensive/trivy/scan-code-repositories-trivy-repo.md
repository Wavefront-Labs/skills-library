---
id: computing-software.cybersecurity-defensive.trivy.scan-code-repositories-trivy-repo
name: scan-code-repositories-trivy-repo
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [trivy-repo, repository, lock-files, scanners, misconfig, license, single-file]
level: intro
status: docs-checked
description: "Scan local or remote git repositories with trivy repo, which targets lock files, and enable the misconfiguration and license scanners that are off by default."
sources:
  - https://trivy.dev/latest/docs/guide/target/repository/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`trivy repo` scans local or remote code repositories for vulnerabilities, misconfigurations, secrets and licenses.

```bash
trivy repo (REPO_PATH | REPO_URL)
trivy repo ./
trivy repo ./trivy-ci-test/Pipfile.lock
trivy repo https://github.com/aquasecurity/trivy-ci-test
```

The second form scans the current directory, the third scans a single file, and the fourth a remote URL.

Rationale: the command is meant for repositories on your machine or in CI. Unlike container or VM image scanning, it targets lock files such as `package-lock.json` and does not target artifacts such as JAR files or other binaries.

Scanner defaults:

| Scanner | Default | How to change |
| --- | --- | --- |
| Vulnerabilities | on | based on lock files such as `Gemfile.lock` |
| Secrets | on | |
| Misconfigurations | off | `trivy repo --scanners misconfig (REPO_PATH \| REPO_URL)` |
| Licenses | off | `trivy repo --scanners license (REPO_PATH \| REPO_URL)` |

You select scanners with `--scanners`. When no OS is detected, a vulnerability scan prints a warning that OS package vulnerabilities are not detected, and then reports language findings per lock file, for example `Pipfile.lock`.

Trivy can also generate an SBOM for code repositories.

## Checked

2026-11-03. Read and confirmed against the Code Repository page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
