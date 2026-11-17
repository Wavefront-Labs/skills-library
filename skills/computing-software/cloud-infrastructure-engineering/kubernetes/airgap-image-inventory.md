---
id: computing-software.cloud-infrastructure-engineering.kubernetes.airgap-image-inventory
name: airgap-image-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, air-gapped, airgap-image-list, image-inventory, image-mirroring, skopeo]
level: practitioner
status: docs-checked
description: "Build a complete image list for an air-gapped cluster from kubeadm, CNI, addon manifests and Helm charts, including init containers and digests."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#without-internet-connection", "https://helm.sh/docs/helm/helm_template/", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md", "https://github.com/containers/skopeo/blob/main/docs/skopeo-inspect.1.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Air-gap image inventory

A missing image is found only when a pod fails with `ImagePullBackOff` inside the air gap.
Build the list mechanically.

## Kubernetes core
```bash
kubeadm config images list --kubernetes-version v<major>.<minor>.<patch> > images.txt
```
Includes apiserver, controller-manager, scheduler, proxy, pause, etcd, coredns. Pass `--config` (with your `imageRepository`) when you mirror to a custom registry; see `kubeadm config images list --config` in the kubeadm-init page.

## Rendered manifests and charts
```bash
helm template cilium cilium/cilium --version <chart-version> -f cilium-values.yaml --include-crds > rendered/cilium.yaml
helm template ingress <repo>/<chart> --version <chart-version> -f ingress-values.yaml > rendered/ingress.yaml
kubectl kustomize overlays/prod > rendered/apps.yaml
# extract every image: value, including initContainers, from all rendered YAML with a YAML-aware tool
# and append them (one per line) to images.txt
```
Render with the SAME values you will deploy: values toggle components (Hubble relay, admission
webhooks with their own `kube-webhook-certgen` image).

## Hidden images
- Images referenced in ConfigMaps or CRDs and pulled by operators at runtime (for example the
  Prometheus operator's config-reloader, cert-manager's acmesolver, Cilium's envoy, CSI
  sidecars). Read operator docs and grep rendered YAML for `image:` in args and env.
- Helm test hooks: `helm template` includes them unless you pass `--skip-tests`; decide deliberately.

## Pin and copy
```bash
sort -u images.txt | while read img; do
  digest=$(skopeo inspect --format '{{.Digest}}' docker://$img)
  echo "$img@$digest"; done > images.lock
sort -u images.txt | while read img; do
  skopeo copy --all --preserve-digests docker://$img docker://registry.internal/${img#*/}; done
```
`skopeo inspect` reports the top-level manifest digest in `Digest`; `--all` copies every architecture in a
manifest list and `--preserve-digests` keeps the digests unchanged. `images.lock` records what was mirrored.

## Verify inside the gap
Deploy to a staging cluster with egress blocked, then:
```bash
kubectl get pods -A -o jsonpath='{range .items[*]}{range .status.containerStatuses[*]}{.image}{"\n"}{end}{end}' | sort -u | grep -v registry.internal
kubectl get events -A --field-selector reason=Failed | grep -i pull
```

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1), kubeadm source, helm-www and skopeo docs: kubeadm config images list --kubernetes-version and --config, helm template flags (--version, -f, --include-crds, --skip-tests), skopeo inspect Digest (top-level manifest), skopeo copy --all and --preserve-digests. Replaced an unverified yq expression and pinned chart versions with placeholders.

Method: documentation only; no commands were run.
