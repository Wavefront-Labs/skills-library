---
id: computing-software.cloud-infrastructure-engineering.docker.run-network-and-security-entitlements
name: run-network-and-security-entitlements
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, run-instruction, run-network-none, run-security-insecure, entitlements, network-host, buildkit]
level: advanced
status: docs-checked
description: "Control network and privileges per RUN step: --network=none for hermetic steps, --network=host and --security=insecure with buildx entitlements and daemon.json."
sources: ["https://docs.docker.com/reference/dockerfile/#run---network", "https://docs.docker.com/reference/dockerfile/#run---security", "https://docs.docker.com/reference/cli/docker/buildx/build/#allow", "https://docs.docker.com/reference/cli/docker/buildx/create/#buildkitd-flags"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RUN --network and --security

## --network
| Value | Effect |
|---|---|
| `default` | The default network for the build (same as no flag) |
| `none` | No network access (`lo` is still available, isolated to this process) |
| `host` | The host's network environment, per instruction; needs the `network.host` entitlement |

Isolating external effects: only the packages shipped with the build can be installed.
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.6
ADD mypackage.tgz wheels/
RUN --network=none pip install --find-links wheels mypackage
```

Host network, similar to `docker build --network=host` but per instruction:
```dockerfile
RUN --network=host pip install -r requirements.txt
```
```bash
# custom builder: allow the entitlement when starting buildkitd, and request it on the build
docker buildx create --name ent --driver docker-container \
  --buildkitd-flags '--allow-insecure-entitlement network.host' --use
docker buildx build --allow network.host .
```
The BuildKit daemon must allow the entitlement (`--allow-insecure-entitlement` flag or the
buildkitd config) and the build request must pass `--allow`.

## --security=insecure
The default mode is `sandbox`. `--security=insecure` runs the step without the sandbox, for flows
that need elevated privileges (the reference gives containerd as an example); it is equivalent
to `docker run --privileged`.
```dockerfile
RUN --security=insecure cat /proc/self/status | grep CapEff
```
```bash
docker buildx create --name priv --driver docker-container \
  --buildkitd-flags '--allow-insecure-entitlement security.insecure' --use
docker buildx build --allow security.insecure .
```
In Bake set `entitlements = ["security.insecure"]` on the target.

## Gotchas
- Both entitlements need two opt-ins: the daemon side (`--allow-insecure-entitlement`) and the
  build request (`--allow`). `buildx build --allow` also lists `device` and
  `buildx.local.delete`; the latter is checked by Buildx itself and not sent to the daemon.
- `--network=host` gives the step the host's network environment; keep it out of release
  pipelines where you want isolation.
- `--security=insecure` is equivalent to `docker run --privileged`; use a dedicated builder.

## Verify
Run the build with `--progress=plain` and confirm the entitled step succeeds with `--allow` and
is refused without it.

## Checked

Checked 2026-10-23 against the Dockerfile reference (`RUN --network`, `RUN --security`; moby/buildkit main branch) and the docker/buildx `build --allow` reference and `buildx bake` reference (main branches).

- `--network` values (`default`, `none`, `host`), the `network.host` and `security.insecure` entitlements and the two-sided opt-in (`--allow-insecure-entitlement` on buildkitd, `--allow` on the build), `--security=sandbox|insecure` equivalent to `--privileged`.
- Bake `entitlements` attribute is a documented override key; `buildx.local.delete` and `device` are also valid `--allow` values.
- Removed the `daemon.json` entitlements block, the labs-frontend history, the quoted entitlement error message, the DNS remark and the `buildx inspect` grep, none of which is in the references.

Method: documentation only; no commands were run.
