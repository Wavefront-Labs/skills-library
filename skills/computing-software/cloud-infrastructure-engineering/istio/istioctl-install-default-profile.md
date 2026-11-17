---
id: computing-software.cloud-infrastructure-engineering.istio.istioctl-install-default-profile
name: istioctl-install-default-profile
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istioctl-install, istio-install, istiod]
level: practitioner
status: docs-checked
description: "Install the Istio control plane with istioctl install, optionally generate the manifest first, and know the caveats of manifest generate."
sources: ["https://istio.io/latest/docs/setup/install/istioctl/", "https://istio.io/latest/docs/setup/additional-setup/config-profiles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`istioctl install` with no flags installs the `default` profile (istiod and istio-ingressgateway, per the profiles table) on the cluster in your Kubernetes configuration. The guide calls it a good starting point for production, unlike the larger `demo` profile.

```sh
istioctl install
istioctl install --set profile=demo
istioctl install --set meshConfig.accessLogFile=/dev/stdout
istioctl install -f my-config.yaml
```

`--set` and an IstioOperator file (`apiVersion: install.istio.io/v1alpha1`, `kind: IstioOperator`) passed with `-f` are equivalent, but `-f` is strongly recommended for production. Legacy Helm `values.yaml` paths work with `--set` when prefixed with `values.`. Prefer the compiled-in charts over `--manifests=<path>` except to experiment.

To review the manifest first: `istioctl manifest generate > $HOME/generated-manifest.yaml` (pass the same flags you would use to install). Caveats the guide lists for installing from a generated manifest: create the Istio namespace manually; the `istiod-default-validator` webhook is only created if `values.defaultRevision` is set; dependency ordering may differ and `kubectl apply` may show transient errors; the method is not tested as part of Istio releases; it runs offline, so use `--cluster-specific` to embed the target cluster's environment; and removed resources (such as a gateway) are not pruned, unlike `istioctl install`.

Uninstall: `istioctl uninstall --purge` removes all Istio resources including shared cluster-scoped ones; the control plane namespace is not removed by default.

## Checked

2026-11-03. Confirmed against the Istio istioctl install guide and the configuration profiles page. Removed: `istioctl x precheck`, `istioctl verify-install`, `istioctl version --remote=false` and pod-readiness verify steps and the claim that an old binary silently installs an old version, none of which the pages cover; the page only says the compiled-in charts ship with the binary.
Method: documentation only; no commands were run.
