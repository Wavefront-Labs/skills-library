---
id: computing-software.cloud-infrastructure-engineering.etcd.discovery-service-bootstrap
name: discovery-service-bootstrap
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [discovery, discovery-url, etcd-discovery, bootstrap, dynamic, token, discovery-fallback]
level: practitioner
status: docs-checked
description: "Bootstrap without knowing member addresses using --discovery with a token URL, such as discovery.etcd.io, and its size parameter."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/clustering/"
  - "https://etcd.io/docs/v3.5/dev-internal/discovery_protocol/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When member IPs are not known up front, members can find each other through a discovery service by using a shared discovery URL.

Create a token URL, specifying the expected cluster size:

```bash
curl https://discovery.etcd.io/new?size=3
# https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

The size defaults to 3 when omitted.

Start each member with that URL:

```bash
etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380   --listen-peer-urls http://10.0.1.10:2380   --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379   --advertise-client-urls http://10.0.1.10:2379   --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

The page's discovery examples do not pass `--initial-cluster`; each member needs a different `--name`, or discovery fails on duplicated names.

How it works (discovery protocol): each member registers itself under the discovery URL, checks the expected size, and waits until enough members have registered; each then bootstraps from the resulting member list, as `--initial-cluster` would. If more than the expected size register, the first N registered form the cluster and the others fail because the cluster is full. You can host your own discovery cluster by setting the `_config/size` key on a private etcd cluster.

Related flags: `--discovery-fallback` (default `proxy`), `--discovery-proxy`.

Properties:

- Discovery is only used for bootstrapping; if a cluster is already initialized etcd logs `discovery token ignored since a cluster has already been initialized`, a harmless warning.
- One discovery token represents one cluster; once the protocol starts on a token, even if it fails halfway, it must not be used for another cluster.
- `ETCD_DISCOVERY_PROXY` / `--discovery-proxy` sets an HTTP proxy to the discovery service.
- Without a `size` configuration the member fails with `the cluster doesn't have a size configuration value`.

## Checked

2026-11-03. Confirmed on the v3.5 clustering guide (etcd discovery) and the discovery protocol page: public service at discovery.etcd.io, curl /new?size=3 with default size 3, --discovery flag, unique names, registration and wait workflow, first N members rule, one token per cluster, discovery URL only for initial bootstrap, the token-ignored warning and size error, and --discovery-fallback (default proxy) and --discovery-proxy on the configuration page. Removed: the do-not-combine rule and production hosting advice, which the pages do not state.

Method: documentation only; no commands were run.
