---
id: computing-software.cloud-infrastructure-engineering.linkerd.custom-cluster-domain-install
name: custom-cluster-domain-install
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, cluster-domain, install, trust-domain]
level: practitioner
status: docs-checked
description: "Install Linkerd, Viz and Multicluster correctly on a cluster with a non-default cluster domain."
sources:
  - https://linkerd.io/2.19/tasks/using-custom-domain/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If the cluster uses a custom cluster domain, install Linkerd with `--cluster-domain`, and set the identity trust domain to match, because mTLS needs the identity trust domain to equal the cluster domain.

```bash
linkerd install --crds | kubectl apply -f -
linkerd install --cluster-domain=example.org \
    --identity-trust-domain=example.org \
    | kubectl apply -f -
```

Extensions need the same setting:

```bash
linkerd viz install --set clusterDomain=example.org | kubectl apply -f -
linkerd multicluster install --set identityTrustDomain=example.org | kubectl apply -f -
```

With these flags Linkerd handles service discovery, routing, service profiles and traffic split resources using the `example.org` domain.

Changing the cluster domain while upgrading Linkerd is not supported,.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/using-custom-domain/.

Removed or reworded: Troubleshooting advice not on the page.

Method: documentation only; no commands were run.
