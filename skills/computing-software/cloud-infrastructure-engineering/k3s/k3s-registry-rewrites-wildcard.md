---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-registry-rewrites-wildcard
name: k3s-registry-rewrites-wildcard
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, registry-rewrite, wildcard-mirror, pull-through-cache]
level: advanced
status: docs-checked
description: "Use redirects, regex rewrites and the quoted wildcard entry in registries.yaml for pull-through caches and renamed projects."
sources:
  - https://docs.k3s.io/installation/private-registry
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Redirects: if a private registry mirrors another (pull-through cache), pulls are redirected transparently. The original registry name is passed to the endpoint in the ns query parameter. With docker.io mapped to https://registry.example.com:5000, pulling docker.io/rancher/mirrored-pause:3.6 fetches registry.example.com:5000/rancher/mirrored-pause:3.6.

Rewrites: regular expressions that transform the image name (not the tag), useful when the project layout differs:

```
mirrors:
  docker.io:
    endpoint:
      - "https://registry.example.com:5000"
    rewrite:
      "^rancher/(.*)": "mirrorproject/rancher-images/$1"
```

This pulls the image as registry.example.com:5000/mirrorproject/rancher-images/mirrored-pause:3.6.

Rewrites for direct pulls: mirror endpoints matching the default endpoint are ignored, and the default is tried last without rewrites. To rewrite a direct pull, list an endpoint that does not match, for example the same host with an explicit port (https://registry.example.com:443).

Images are still stored under the original name: `crictl image ls` shows docker.io/rancher/mirrored-pause:3.6.

Wildcard: a "*" entry (quoted, the asterisk MUST be quoted) in mirrors and configs gives defaults for all registries, used only if there is no specific entry. Example: one mirror for everything and `insecure_skip_verify: true` for all except docker.io.

## Checked

2026-11-08. Read the full K3s Private Registry Configuration page (docs/installation/private-registry.md in the k3s-io/docs repo). Confirmed: ns query parameter redirects, rewrite regex example and resulting image name, rewrites applying to the name not the tag, default endpoint matching rule and the explicit port workaround, images stored under the original name, and the quoted wildcard entry. Nothing removed.

Method: documentation only; no commands were run.
