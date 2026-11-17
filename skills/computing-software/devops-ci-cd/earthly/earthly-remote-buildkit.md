---
id: computing-software.devops-ci-cd.earthly.earthly-remote-buildkit
name: earthly-remote-buildkit
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, remote-buildkit, buildkitd, buildkit-host, buildkit-tcp-transport-enabled, buildkit-tls-enabled, mtls, tlsca]
level: advanced
status: docs-checked
description: "Self-host a remote earthly/buildkitd: ports 8371-8373, /tmp/earthly volume, BUILDKIT_TCP_TRANSPORT_ENABLED, BUILDKIT_TLS_ENABLED, client buildkit_host and tls settings."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/remote-buildkit.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remote BuildKit (self-hosted)

Goal: run `earthly/buildkitd` on another machine so builds share its cache instantly, instead of uploading/downloading cache. Self-Hosted Satellites (beta) are the suggested alternative; remote BuildKit remains supported if you cannot use a cloud control plane.

## Daemon side
- Open ports `8371-8373`.
- Mount `/tmp/earthly` (the BuildKit cache location) as a Docker volume; the docs strongly recommend it, else excess disk use, slowness or malfunction (and, in some environments, "rm: can't remove '/var/earthly/dind/...': Resource busy").
- `BUILDKIT_TCP_TRANSPORT_ENABLED`: makes buildkitd listen on port 8372 (remap at the port-mapping level for another external port). TCP is required for sharing a daemon.
- `BUILDKIT_TLS_ENABLED`: set `true` for any daemon handling production workloads; the daemon is by design an arbitrary code execution machine, so mTLS is recommended. Mount certificates and keys at `/etc/*.pem`.

## Client side
Earthly then will not manage the daemon. Set:
- `buildkit_host`, e.g. `tcp://my-cool-remote-daemon:8372`. IPv6 loopback, `127.0.0.1` and localhost count as "local"; the machine hostname does not.
- `tlsca`, `tlscert`, `tlskey`: paths to the client certificates for an mTLS daemon, relative to the Earthly config unless absolute.
- `tls_enabled`: on by default (except for a local buildkit container); set `false` to disable.

## Local-Remote
You can use TCP and mTLS against a daemon container Earthly still manages: it optionally generates its own certificates and connects via `tcp://127.0.0.1:8372`, a way to test remote features without separate machines.

## Kubernetes caveats (experimental)
Multiple buildkitd instances: cache is not shared (slow to warm), simultaneous builds across instances may fail, TLS config must be shared. Keep a build on one instance with session affinity:
```yaml
sessionAffinity: ClientIP
sessionAffinityConfig:
  clientIP:
    timeoutSeconds: 600 # This should be longer than your build.
```

## Gotcha
A single remote `earthly/buildkitd` in privileged mode with an unprivileged `earthly/earthly` pod is experimental.

## Checked

2026-11-07. Read docs/ci-integration/remote-buildkit.md and docs/ci-integration/guides/kubernetes.md in full. Ports, env vars, client config keys, Local-Remote and Kubernetes caveats match. Removed: the example of setting buildkit_host with earthly config in a container image (on neither page).
Method: documentation only; no commands were run.
