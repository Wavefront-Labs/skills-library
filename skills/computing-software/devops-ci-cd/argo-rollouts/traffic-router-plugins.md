---
id: computing-software.devops-ci-cd.argo-rollouts.traffic-router-plugins
name: traffic-router-plugins
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [plugin, traffic-router, go-plugin, argo-rollouts-config, configmap, gateway-api, argo-rollouts]
level: sme
status: docs-checked
description: "Install a third-party traffic router plugin through the argo-rollouts-config ConfigMap using a file or HTTP location."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Traffic router plugins (an experimental, alpha-quality feature since 1.5.0) support routers not built in. The docs say the plugin system uses the go-plugin library.

Two install methods, both configured in the `argo-rollouts-config` ConfigMap (a `trafficRouterPlugins` entry, with `name` and `location`):

1. **Mount the executable** into the controller container: init container downloader, shared volume (NFS, EBS), or build into the image; point `location` at `file://...`.
2. **Host on HTTP(S)**: `location` is an http(s) URL, with an optional `sha256` checksum of the executable and optional download headers taken from a Secret via `headersFrom` and `secretRef`.

```yaml
data:
  trafficRouterPlugins: |-
    - name: "argoproj-labs/sample-nginx"
      location: "https://example.com/plugin-linux-amd64"
      sha256: "<checksum>"
```

The `name` must match the name the plugin requires so it can find its configuration.

Warning from the docs: the controller will not start if it cannot download or find the plugin executable. It downloads once at startup, so HA mode helps because other replicas already have the binary during a server outage.

Plugins listed in the docs include a sample nginx plugin (not meant for production), Consul, Contour, Gateway API (Kuma, Traefik, Cilium, Contour, HAProxy and others), Gloo Edge, Gloo Platform and OpenShift Route.

Verify the controller pod starts; it will not start if it cannot download or find the plugin executable.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/plugins/.

Removed or corrected: the beta label and stable-interface claim (the page says alpha), the trafficRouting.plugins selection claim, the Gloo Gateway and kgateway names.

Method: documentation only; no commands were run.
