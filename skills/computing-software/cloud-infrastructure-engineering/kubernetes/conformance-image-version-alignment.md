---
id: computing-software.cloud-infrastructure-engineering.kubernetes.conformance-image-version-alignment
name: conformance-image-version-alignment
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, conformance, conformance-image, sonobuoy, hydrophone, kubernetes-version]
level: practitioner
status: docs-checked
description: "Run the conformance suite with the image that matches the cluster's Kubernetes version, and spot results invalidated by a mismatch."
sources: ["https://github.com/cncf/k8s-conformance/blob/master/instructions.md", "https://sonobuoy.io/docs/main/cli/sonobuoy_run/", "https://sonobuoy.io/docs/main/airgap/", "https://github.com/kubernetes-sigs/hydrophone/blob/main/docs/quickstart.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conformance image and version alignment

The e2e conformance tests ship in `registry.k8s.io/conformance:v<version>`. Running tests
from another minor version checks behaviour the cluster was never meant to have (or misses new
required tests), and the CNCF submission checks reject results whose Kubernetes version does
not match the release folder or that lack required tests.

## sonobuoy
```bash
kubectl version -o json | jq -r .serverVersion.gitVersion
sonobuoy run --mode=certified-conformance \
  --kubernetes-version <vX.Y.Z>                       # overrides the version of the default e2e image
# or name the image explicitly
sonobuoy run --mode=certified-conformance --kube-conformance-image registry.k8s.io/conformance:<vX.Y.Z>
```
By default `--kubernetes-version` is `auto`: Sonobuoy uses the cluster's detected version and
errors if it cannot detect one (`ignore` tries resolution but ignores errors).

## hydrophone
```bash
hydrophone --conformance --conformance-image registry.k8s.io/conformance:<vX.Y.Z>
```

## Air-gapped
Mirror the conformance image and the e2e test images: `sonobuoy images pull`, then
`sonobuoy images push --e2e-repo <registry>` (or `--e2e-repo-config <file>`), and run with
the same `--e2e-repo` / `--e2e-repo-config` flag. `sonobuoy images list` shows the images.

## Signs of a mismatch
- Failures about API fields or kinds that do not exist in your version.
- The CNCF checks report missing required tests or a version that does not match the folder.

## Verify
`sonobuoy results $(sonobuoy retrieve)` and confirm the tested version equals the server version.

## Checked
Checked 2026-10-27 against the Sonobuoy CLI reference (`run --kubernetes-version` default
`auto`, `--kube-conformance-image`, `images list/pull/push`), the Sonobuoy air-gap guide
(`--e2e-repo`, `--e2e-repo-config`), the Hydrophone quickstart (`--conformance-image`) and
cncf/k8s-conformance instructions.md (version and required-test checks). Corrected the Sonobuoy
image flag (`--conformance-image` is Hydrophone's; Sonobuoy uses `--kube-conformance-image`);
removed the unconfirmed vendor-suffix behaviour and pinned example versions.

Method: documentation only; no commands were run.
