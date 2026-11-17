---
id: computing-software.cloud-infrastructure-engineering.linkerd.upgrade-linkerd-cli-flow
name: upgrade-linkerd-cli-flow
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, upgrade, cli, crds, prune]
level: practitioner
status: docs-checked
description: "Upgrade Linkerd in sequence: CLI, CRDs and control plane, prune, extensions, data plane, with checks before and after."
sources:
  - https://linkerd.io/2.19/tasks/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrade components in this order: the CLI, the control plane, the extensions, then the data plane. During an upgrade the control plane runs the new version while the data plane lags. It is usually safe for the control plane to be ahead of the data plane by up to a full version, but read the release notes first.

Before starting, run `linkerd check`, and for major version upgrades `linkerd check --proxy` to avoid unintended skew. Confirm Linkerd and Kubernetes versions are compatible.

CLI:

```bash
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install-edge | sh
linkerd version --client
```

Control plane (CLI installs) retains existing configuration and TLS secrets. Upgrade CRDs first, then the control plane, then remove resources no longer needed:

```bash
linkerd upgrade --crds | kubectl apply -f -
linkerd upgrade | kubectl apply -f -
linkerd prune | kubectl delete -f -
linkerd check
```

Helm installs follow the Helm upgrade procedure instead. Edge releases are not semantically versioned, so use the release notes to find breaking changes, and the Releases and Versions page to map an edge release to a Linkerd version.

Extensions: the extension CLI commands have no upgrade subcommands, so run install again, for example `linkerd viz install | kubectl apply -f -`, and use the extension's `prune` command (for example `linkerd viz prune | kubectl delete -f -`).

Data plane: pods are immutable, so restart each workload, for example `kubectl -n <namespace> rollout restart deploy`, and the injector adds the latest proxy. A skew of one major version between data plane and control plane is supported; more than one is not. Verify with `linkerd check --proxy`, which lists pods still running older proxies.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/tasks/upgrade/. Upgrade order, skew guidance, pre-checks, CLI install and version commands, the CRD-then-control-plane-then-prune sequence, Helm pointer, edge release versioning, extension and data plane steps.

Removed or reworded: Nothing.

Method: documentation only; no commands were run.
