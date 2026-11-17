---
id: computing-software.cloud-infrastructure-engineering.etcd.versioning-and-support-policy
name: versioning-and-support-policy
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [versioning, support-policy, release-branches, semver, patch-releases, api-versioning, supported-versions]
level: intro
status: docs-checked
description: "etcd versions follow semantic versioning; the project supports the current minor release and the two before it."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/versioning/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd versions are x.y.z: x is the major version, y the minor and z the patch, following Semantic Versioning terminology.

- New minor versions may add features to the API.
- The project maintains release branches for the current version and two previous releases. When v3.7 is current, v3.6 and v3.5 are supported; when v3.8 is released, v3.5 goes out of support.
- Applicable fixes, including security fixes, may be backported to those three release branches, depending on severity and feasibility. Patch releases are cut from those branches when required. The project Maintainers own this decision.
- The v3 API responses should not change after the 3.0.0 release, but new features are added over time.

Check the version of a running cluster with etcdctl:

```bash
etcdctl --endpoints=127.0.0.1:2379 endpoint status
```

## Checked

2026-11-08. Read in full: etcd v3.5 Versioning page. Confirmed every statement above. Removed: etcd --version, per-member and cluster version semantics of endpoint status, the one-minor-at-a-time upgrade rule and latest-patch advice (not on the page); dropped the FAQ source, which supported nothing here.
Method: documentation only; no commands were run.
