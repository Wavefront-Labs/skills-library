---
id: computing-software.cloud-infrastructure-engineering.docker.minifying-images-with-slimtoolkit
name: minifying-images-with-slimtoolkit
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-slimming, slimtoolkit, docker-slim, slim-build, xray, dynamic-analysis]
level: advanced
status: gated
description: "Minify an existing image with slimtoolkit (formerly docker-slim): slim build with HTTP probes, include paths, xray inspection, and testing that nothing needed was removed."
sources: ["https://github.com/slimtoolkit/slim", "https://github.com/slimtoolkit/slim#build-command-options", "https://github.com/slimtoolkit/slim#xray-command-options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minifying images with slimtoolkit

`slim` runs your container, watches which files it touches (fanotify + ptrace) while probes
exercise it, then builds a new image containing only those files. Gains of 10-30x are common
for fat language images. The risk: anything not exercised is deleted.

## Install and run
```bash
curl -sL https://raw.githubusercontent.com/slimtoolkit/slim/master/scripts/install-slim.sh | sudo -E bash -
# or containerised:
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock dslim/slim build ...
```
```bash
slim build --target myapp:1.4 --tag myapp:1.4-slim \
  --http-probe=true --http-probe-cmd /healthz --http-probe-cmd /api/v1/items \
  --expose 8080 \
  --include-path /etc/ssl/certs \
  --include-path /app/templates \
  --include-bin /usr/bin/curl \
  --continue-after probe
```
Key flags:
| Flag | Purpose |
|---|---|
| `--http-probe` / `--http-probe-cmd` / `--http-probe-cmd-file` | Exercise endpoints during analysis |
| `--exec "sh -c '...'"` | Run a command inside the container as the probe (CLIs, workers) |
| `--continue-after enter|probe|exec|timeout` | When to stop collecting |
| `--include-path`, `--include-bin`, `--include-shell` | Force-keep files the probe will not hit |
| `--env`, `--mount`, `--network` | Run-time context the app needs to start |
| `--copy-meta-artifacts ./slim-report` | Keep the report and generated seccomp/AppArmor profiles |

## Inspect first
```bash
slim xray --target myapp:1.4      # layers, files, ENTRYPOINT, shells present; no changes made
```

## Making it safe
- Run the full integration suite against the `-slim` tag in CI; a smoke test is not enough.
  Lazy-loaded plugins, locale data, timezone files and error templates are typical casualties.
- Commit the include lists as a file (`--include-path-file`) next to the Dockerfile.
- Re-slim on every base image update; the output is not stable across upstream changes.
- Prefer fixing the Dockerfile (multi-stage, distroless) when possible; slim is best for
  images you do not control or legacy apps.

## Gotchas
- Needs access to the Docker socket and runs the image: do not slim untrusted images on a
  shared host.
- Shells are removed by default, so `docker exec sh` and shell-form `CMD` break; add
  `--include-shell` if needed.
- The generated seccomp profile only allows observed syscalls; use it only after broad testing.

## Verify
```bash
docker image ls myapp
docker run --rm -p 8080:8080 myapp:1.4-slim & ./run-integration-tests.sh http://localhost:8080
```

## Checked

- Date: 2026-11-02.
- Confirmed against: slim build flags --target, --tag, --http-probe, --http-probe-cmd, --continue-after, --copy-meta-artifacts and the install script URL (slimtoolkit README).
- Not confirmed: the exec forms in the example test script (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
