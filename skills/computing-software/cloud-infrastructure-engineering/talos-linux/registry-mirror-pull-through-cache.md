---
id: computing-software.cloud-infrastructure-engineering.talos-linux.registry-mirror-pull-through-cache
name: registry-mirror-pull-through-cache
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [registry-mirror, pull-through-cache, registrymirrorconfig, harbor, registryauthconfig, containerd]
level: practitioner
status: docs-checked
description: "Redirect image pulls to local registries with RegistryMirrorConfig: per-endpoint mirrors, skipFallback, overridePath for Harbor, plus RegistryAuthConfig and RegistryTLSConfig."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/images-container-runtime/pull-through-cache.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Registry mirrors let Talos pull official image references through local caching proxies; the first pull fetches upstream and caches, later pulls are local. The Docker `registry:2` image works as a pull-through cache but needs one container per upstream:

```bash
docker run -d -p 5000:5000 \
    -e REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io \
    --restart always \
    --name registry-docker.io registry:2
```

(repeat for `registry.k8s.io`, `gcr.io`, `ghcr.io` on their own ports). Point Talos at them with one `RegistryMirrorConfig` per upstream; `name` is the leftmost part of the image reference (include the port if present; Docker Hub defaults to `docker.io`):

```yaml
apiVersion: v1alpha1
kind: RegistryMirrorConfig
name: docker.io
endpoints:
    - url: http://10.5.0.1:5000
```

Endpoints are tried in order, with the original upstream as an implicit last endpoint. Stop that fallback with `skipFallback: true`. Talos appends `/v2` to the URL; when the mirror path already contains it (Harbor, which puts the proxy project in the path) set `overridePath: true`:

```yaml
apiVersion: v1alpha1
kind: RegistryMirrorConfig
name: docker.io
endpoints:
    - url: http://harbor/v2/proxy-docker.io
      overridePath: true
```

Mirror credentials and TLS apply to the endpoint URL hostname (include the port if any), not to the image endpoint:

```yaml
apiVersion: v1alpha1
kind: RegistryAuthConfig
name: my-private-registry.io
username: username
password: "****"
```

`RegistryTLSConfig` takes a `ca: |-` PEM block for self-signed registries. The settings are honoured by Talos and propagated to containerd.

## Checked

2026-11-04. Registry containers, RegistryMirrorConfig fields, fallback and overridePath behaviour, Harbor example, auth and TLS documents confirmed on the Pull Through Image Cache page.

Method: documentation only; no commands were run.
