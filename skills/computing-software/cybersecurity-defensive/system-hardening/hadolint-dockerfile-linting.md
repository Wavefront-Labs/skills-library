---
id: computing-software.cybersecurity-defensive.system-hardening.hadolint-dockerfile-linting
name: hadolint-dockerfile-linting
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [hadolint, dockerfile, container-hardening, shellcheck, ci-linting, image-security]
level: practitioner
status: gated
description: "Lint Dockerfiles with hadolint: security-relevant rules, configuration and trusted registries, inline ignores, CI and pre-commit integration, and what it misses."
sources: ["https://github.com/hadolint/hadolint", "https://github.com/hadolint/hadolint#rules", "https://docs.docker.com/build/building/best-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dockerfile linting with hadolint

hadolint parses Dockerfiles into an AST, applies its own `DL` rules and runs ShellCheck (`SC` rules) on `RUN`
instructions. Cheap to run on every commit, it catches insecure and non-reproducible patterns before an image is
built.

## Run
```bash
hadolint Dockerfile
docker run --rm -i hadolint/hadolint < Dockerfile              # (gated: unconfirmed, Docker not available here)
hadolint --format sarif Dockerfile > hadolint.sarif     # for GitHub code scanning
hadolint -c .hadolint.yaml Dockerfile                    # or rely on auto-discovery of $PWD/.hadolint.yaml, XDG and $HOME locations
```
Exit code is 1 when any finding at or above `failure-threshold` (default `info`, so even DL3015-style info findings fail) exists; `--no-fail` forces 0. Checked on hadolint 2.15.1 (Windows binary).

## Security-relevant rules
- **DL3002** Last USER should not be root (default severity warning). It fires only on an explicit `USER root` as the last user; a Dockerfile with no USER at all was NOT flagged (checked), so require a non-root USER with a separate check.
- **DL3007** Using `latest` tag; **DL3006** always tag the image version explicitly (pin; better pin digests).
- **DL3008/DL3018/DL3013/DL3016** pin versions in `apt-get`, `apk`, `pip`, `npm` installs (reproducibility,
  supply chain).
- **DL3020** use COPY instead of ADD for files and folders (error). Checked: `ADD app.py /app/` is flagged, while `ADD http://...tgz` and `ADD app.tar` (URL and archive, which ADD legitimately handles) were not.
- **DL3004** do not use sudo (error).
- **DL3026** use only allowed registries (with `trustedRegistries` configured).
- **DL4006** set `SHELL -o pipefail` before RUN with pipes (otherwise `curl ... | sh` failures are hidden).
- **DL3009** (apt lists) / **DL3019** (apk `--no-cache`) clean package caches (both info level) (smaller images, fewer files).
- **SC2086** etc.: unquoted variables in RUN scripts.

## Configuration (.hadolint.yaml)
```yaml
failure-threshold: warning
trustedRegistries:
  - registry.example.com
  - docker.io/library
override:
  error: [DL3002, DL3007, DL3020, DL3026]
ignored: [DL3059]          # multiple consecutive RUN (style)
label-schema:
  maintainer: text
```
Inline ignore, line before the instruction: `# hadolint ignore=DL3008`. A reason may follow only after a SECOND `#`: `# hadolint ignore=DL3008 # pins managed by renovate`.
The `-- reason` style does NOT work: checked, `# hadolint ignore=DL3018 -- reason` still reported DL3018, while the `# reason` form suppressed it.
Use `# hadolint global ignore=DL3059` to cover the whole file. Inline ignores themselves are rule DL1001 (ignored by default).
A config file in the current directory is picked up automatically (checked: DL3026 and the error overrides applied without `-c`).

## CI and pre-commit
- GitHub Action `hadolint/hadolint-action` with `failure-threshold: error`, SARIF upload (action not run here: gated: unconfirmed, no GitHub Actions run).
- pre-commit hooks `hadolint-docker` and `hadolint` exist in the hadolint repo's `.pre-commit-hooks.yaml` (`hadolint` needs the binary installed).
- Lint all Dockerfiles (`find . -name 'Dockerfile*'`), including CI images.

## What it does not catch
Secrets in layers (use secret scanners, BuildKit secrets), vulnerable packages (Trivy/Grype image scan), runtime
settings (capabilities, read-only FS - check with Kubernetes policy and Docker Bench). Pair with Trivy's
misconfiguration scanner or Checkov for overlapping Dockerfile checks.

## Verify
CI fails a test Dockerfile with `FROM node:latest` (DL3007) or `USER root` last (DL3002); existing Dockerfiles pass at the configured
threshold with justified ignores only.
