---
id: computing-software.cybersecurity-defensive.trivy.scan-local-projects-trivy-fs
name: scan-local-projects-trivy-fs
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [trivy-fs, filesystem-scan, lock-files, scanners, scan-cache, git-repository]
level: practitioner
status: docs-checked
description: "Scan a project directory or single lock file with trivy fs, choosing which of vulnerability, misconfiguration, secret and license scanners run."
sources:
  - https://trivy.dev/latest/docs/guide/target/filesystem/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`trivy fs` scans local projects for vulnerabilities, misconfigurations, secrets and licenses. Point it at a directory or a single file:

```bash
trivy fs /path/to/project
trivy fs <path>/Pipfile.lock
```

Scanner defaults and how to change them with `--scanners`:
- vulnerabilities: on by default; found from lock files such as `Gemfile.lock` and `package-lock.json`;
- secrets: on by default;
- misconfigurations: off, enable with `--scanners misconfig`;
- licenses: off, enable with `--scanners license`.

So `trivy fs --scanners misconfig /path/to/project` runs only misconfiguration scanning. A warning that the OS is not detected is normal for a project directory, since OS package vulnerabilities are not detected there.

SBOM generation works on local projects too (see the SBOM pages).

Scan cache: the filesystem target does not use the cache by default. When the project is a git repository with clean status and a cache backend other than memory is enabled, Trivy stores analysis results keyed by the latest commit hash:

```shell
trivy fs --cache-backend fs /path/to/git/repo
```

Use `trivy fs` for local projects in CI/CD; `trivy rootfs` is for host or unpacked root filesystems and behaves differently.

## Checked

2026-11-03. Read and confirmed against the Filesystem page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
