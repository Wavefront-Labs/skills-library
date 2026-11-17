---
id: computing-software.cybersecurity-defensive.trivy.secret-scanning-quick-start
name: secret-scanning-quick-start
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [secret-scanning, secrets, builtin-rules, scanners, base-image-layers]
level: intro
status: docs-checked
description: "Secret scanning is on by default in Trivy; scan images and filesystems for keys and tokens, see the report columns, and turn it off with --scanners."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/secret/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy scans container images, filesystems and git repositories for exposed secrets such as passwords, API keys and tokens. Secret scanning is enabled by default. Trivy scans every plaintext file according to built-in rules or your configuration, and can also detect secrets in compiled Python files (`.pyc`). Built-in rules cover, among others, AWS access keys, GCP service accounts, GitHub and GitLab personal access tokens, and Slack access tokens.

If a secret is not detected, check that its file is not in the built-in allowed paths. You can disable allow rules with `disable-allow-rules`.

Container image: pass an image name.

```shell
trivy image myimage:1.0.0
```

Findings appear as a separate section such as `app/secret.sh (secrets)` with the columns CATEGORY, DESCRIPTION, SEVERITY, LINE NO and MATCH; the match value is masked, for example `export AWS_ACCESS_KEY_ID=*****`.

Filesystem:

```shell
trivy fs /path/to/your_project
```

A private key file reports as category `AsymmetricPrivateKey`, severity HIGH.

Trivy tries to detect a base image and skip its layers for secret scanning, because base images contain many files and slow scanning. If a secret is missed, run with `--debug` to see the base layers.

To disable secret scanning entirely, restrict scanners:

```shell
trivy image --scanners vuln alpine:3.15
```

## Checked

2026-11-03. Read and confirmed against the Secret Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
