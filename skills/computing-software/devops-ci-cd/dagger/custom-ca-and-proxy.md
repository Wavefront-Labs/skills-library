---
id: computing-software.devops-ci-cd.dagger.custom-ca-and-proxy
name: custom-ca-and-proxy
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, custom-ca, proxy, certificates, networking, engine]
level: practitioner
status: docs-checked
description: "Make the Dagger Engine trust custom certificate authorities and use HTTP(S) proxies, including how both reach user containers."
sources: [https://docs.dagger.io/0.21/reference/configuration/custom-ca, https://docs.dagger.io/0.21/reference/configuration/proxy, https://docs.dagger.io/0.21/reference/configuration/engine]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom CAs and proxies for the Dagger Engine

Goal: let Dagger reach registries, Git hosts and other services behind corporate TLS interception or proxies. Dagger 0.21 docs.

## Custom CAs

- Auto-provisioned engine: put certificates in `~/.config/dagger/ca-certificates` (Linux), `~/Library/Application Support/dagger/ca-certificates` (macOS) or `$XDG_CONFIG_HOME/dagger/ca-certificates` if set. Dagger detects and installs them in the engine.
- Custom engine: place them in `/usr/local/share/ca-certificates/` inside the engine container; they are installed on startup with no further commands:

```shell
docker run --rm \
    -v /var/lib/dagger \
    -v $PWD/ca-certificates:/usr/local/share/ca-certificates/ \
    --name dagger-engine-custom \
    --privileged \
    registry.dagger.io/engine:v<version>
```

- User containers (`withExec`): best-effort automatic install, for Alpine, Debian-based (debian, ubuntu) and Red Hat-based (rhel, fedora, centos) images. Failure is logged and execution continues; CAs are removed when the container exits so they do not leak into cache or published images.
- Registry-specific CA paths can be referenced from engine.json (see computing-software.devops-ci-cd.dagger.engine-config-cache-gc).

## Proxies

Supported variables: `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `ALL_PROXY`, `FTP_PROXY`, plus `_DAGGER_ENGINE_SYSTEMENV_GOPROXY` (propagated only to `GOPROXY` for Go modules). Setting them currently requires provisioning a custom engine and setting the variables on that container.

## Gotchas

- The proxy variables are also set on every `withExec` container; they do not affect cache keys, and changing them does not invalidate the cache. An explicit `withEnvVariable` for the same name overrides the inherited value.
- CAs and proxies cannot be set via engine.json or engine.toml.

## Checked

2026-11-07

Read in full from the docs source: reference/configuration/custom-ca.mdx and proxy.mdx. Added reference/configuration/engine as a source after reading it: it confirms registry CA paths via engine.json and that proxies and CAs cannot be set via engine.json or engine.toml. All paths, proxy variables and container behaviour match the pages.

Method: documentation only; no commands were run.
