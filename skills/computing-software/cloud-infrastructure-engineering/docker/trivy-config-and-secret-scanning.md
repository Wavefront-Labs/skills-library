---
id: computing-software.cloud-infrastructure-engineering.docker.trivy-config-and-secret-scanning
name: trivy-config-and-secret-scanning
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, trivy, trivy-config, trivy-secret, misconfiguration, dockerfile-lint, vulnerability-scanning]
level: practitioner
status: docs-checked
description: "Scan Dockerfiles and Compose files for misconfigurations with trivy config, and images or repos for secrets with --scanners secret; severity gates, skips and custom checks."
sources: ["https://trivy.dev/latest/docs/scanner/misconfiguration/", "https://trivy.dev/latest/docs/scanner/secret/", "https://github.com/aquasecurity/trivy-checks/tree/main/checks/docker", "https://github.com/aquasecurity/trivy-action"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# trivy config and secret scanning

CVE scanning finds vulnerable packages. Two other Trivy scanners catch mistakes CVE scans
miss: insecure Dockerfile/Compose settings and embedded credentials.

## Misconfiguration scanning
```bash
trivy config .                                    # Dockerfile, compose, k8s, terraform, ...
trivy config --severity HIGH,CRITICAL --exit-code 1 .
trivy config -f json -o misconfig.json Dockerfile
trivy image --scanners misconfig myapp:1.4        # checks the image config (user, healthcheck)
```
Built-in Dockerfile checks (IDs `DS-00xx`, also written `AVD-DS-00xx`) include: image user
root (`DS-0002`), `ADD` instead of `COPY` (`DS-0005`), `:latest` tag (`DS-0001`), no `HEALTHCHECK`
(`DS-0026`), `apt-get` without `--no-install-recommends`, `RUN` using `sudo` (`DS-0010`), port 22
exposed (`DS-0004`) and `RUN cd` instead of `WORKDIR` (`DS-0013`).

Suppress with justification in a `.trivyignore` file (default name, set with `--ignorefile`) by
listing the check ID, or with `--skip-files`/`--skip-dirs`. A YAML ignore file can record an
`expired_at` date (`yyyy-mm-dd`) per finding; after that date the ignore stops applying.

Custom organisation rules: write Rego checks and pass `--config-check ./policies` (paths to
Rego files or directories) with `--check-namespaces user` to include your namespace.

## Secret scanning
```bash
trivy fs --scanners secret .                      # repository / build context
trivy image --scanners secret myapp:1.4           # image layers
trivy image --scanners vuln,secret,misconfig myapp:1.4
```
Trivy ships built-in secret rules. Tune with `trivy-secret.yaml` (the default file name in the
current directory, or `--secret-config`): custom `rules`, `allow-rules` (global or per rule),
`enable-builtin-rules` or `disable-rules` (for example `slack-access-token`); if both are given,
`disable-rules` takes precedence.

## CI gate
```yaml
- uses: aquasecurity/trivy-action@v0.36.0
  with:
    scan-type: config
    scan-ref: .
    severity: HIGH,CRITICAL
    exit-code: "1"
```

## Gotchas
- Trivy tries to detect the base image and skips its layers for secret scanning, because base images contain many files and slow the scan; use `--debug` to see skipped base layers.
- Document each ignored check with a reason rather than skipping whole paths.
- Compare with `docker build --check`, which runs BuildKit's own Dockerfile checks without
  installing anything.

## Checked
Documentation release: aquasecurity/trivy docs (main, CLI reference for `trivy image` and `trivy config`, secret scanning, filtering pages), aquasecurity/trivy-checks docker checks and aquasecurity/trivy-action v0.36.0 README, checked 2026-10-26.
Confirmed: `--scanners`, `--severity`, `--exit-code`, `--format`, `--skip-files`, `--skip-dirs`, `--ignorefile` (default `.trivyignore`), `--config-check`, `--check-namespaces`, `--secret-config` (default `trivy-secret.yaml`); check IDs DS-0001, DS-0002, DS-0004, DS-0005, DS-0010, DS-0013 and DS-0026 from the trivy-checks sources; base-image layer skipping for secrets; secret-config rule keys.
Corrected: IDs use the `DS-00xx` form; `--namespaces` is now `--check-namespaces`; action pinned to the README's `v0.36.0`; the inline `# trivy:ignore:` Dockerfile comment, "including deleted files" and the `docker build --check` comparison were not in the sources read and were removed.
Method: documentation only; no commands were run.
