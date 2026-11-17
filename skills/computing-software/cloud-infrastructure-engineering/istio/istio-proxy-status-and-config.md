---
id: computing-software.cloud-infrastructure-engineering.istio.istio-proxy-status-and-config
name: istio-proxy-status-and-config
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, proxy-status, proxy-config, xds-sync]
level: practitioner
status: docs-checked
description: "Check whether every Envoy is in sync with istiod using proxy-status, and inspect clusters, listeners and routes with proxy-config."
sources: ["https://istio.io/latest/docs/ops/diagnostic-tools/proxy-cmd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`proxy-status` shows each proxy's xDS sync state for CDS, LDS, EDS and RDS and the istiod instance it is connected to.

```sh
istioctl proxy-status
istioctl proxy-config cluster deploy/web.shop
istioctl proxy-config listener deploy/web.shop --port 15006
istioctl proxy-config route deploy/web.shop -o json
istioctl proxy-config endpoint deploy/web.shop --cluster "outbound|8080||api.shop.svc.cluster.local"
```

Gotchas: `SYNCED` means Envoy has acknowledged the last configuration istiod sent. `NOT SENT` means istiod has not sent anything, usually because it has nothing to send. `STALE` means istiod sent an update but has not received an acknowledgement, which usually indicates a networking issue between Envoy and istiod or a bug in Istio itself.

Verify: all proxies show `SYNCED` for CDS, LDS, EDS and RDS.

## Checked

2026-11-03. Confirmed in the Istio proxy-cmd debugging page: the `proxy-status` columns and the `SYNCED`, `NOT SENT` and `STALE` definitions, and `proxy-config` listeners/routes/cluster/endpoints with `--port`, `--cluster` and `-o json`. Removed: the invalid-config-rejected explanation of `STALE`, the revision-column claim (the column shows the istiod pod), the large-mesh output remark, the route-appears-within-seconds check and the change-window advice.

Method: documentation only; no commands were run.
