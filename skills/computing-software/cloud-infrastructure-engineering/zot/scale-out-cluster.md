---
id: computing-software.cloud-infrastructure-engineering.zot.scale-out-cluster
name: scale-out-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, scale-out, cluster-members, hash-key, siphash, repo-sharding]
level: advanced
status: docs-checked
description: "Scale Zot across instances (v2.1.0+) where each repo is owned by one instance via SipHash: cluster config, shared storage and cache, failure and limits."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/scaleout.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
How it works: each repository is served by one instance, and only that instance may write it. A receiving instance hashes the repo path (SipHash) and checks its hash table; if another instance owns the repo it forwards the request and proxies the response back, otherwise it handles it locally. Built in from v2.1.0. This is not HA: an instance or storage going offline affects availability.

The `cluster` section:
- `members`: every peer including the instance itself (addresses or hostnames); ordering must be identical on all instances.
- `hashKey`, and a TLS certificate for peer authentication (`cluster.tls.cacert` in the samples).

Compute-only scale-out: all instances share the same cache and S3-compatible storage; each has its own IP, same port by convention. Samples use `dedupe: false`, `remoteCache: true`, an S3 `storageDriver` and a `cacheDriver` of `dynamodb` or `redis`.

Compute and storage scale-out: cache and storage are local to each instance; no cache or storage driver; the UI is not supported.

Traffic: a single load balancer needing no repo-specific rules (any instance can route), or DNS-based balancing (may not suit sticky sessions).

Failure: not self-healing. Only repos mapped to the failed instance are affected; if the error is not transient, resize and restart the cluster without it.

Not supported or special: CVE scanning (use a separate instance outside the cluster), the trust extension (shared directory). Sync works; only the owning instance syncs a repo.

## Checked

2026-11-04. Read against the zot scale-out article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
