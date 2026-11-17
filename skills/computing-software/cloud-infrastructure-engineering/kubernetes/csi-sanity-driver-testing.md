---
id: computing-software.cloud-infrastructure-engineering.kubernetes.csi-sanity-driver-testing
name: csi-sanity-driver-testing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, csi, csi-sanity, csi-test, driver-development, e2e-storage]
level: practitioner
status: docs-checked
description: "Test a CSI driver against the spec with csi-sanity, then run the Kubernetes external storage e2e suite with a test driver definition."
sources: ["https://github.com/kubernetes-csi/csi-test/tree/master/cmd/csi-sanity", "https://github.com/kubernetes/kubernetes/tree/master/test/e2e/storage/external", "https://kubernetes-csi.github.io/docs/functional-testing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# csi-sanity and storage e2e for driver developers

## csi-sanity: gRPC-level spec tests
Download `csi-sanity` from the csi-test Releases page, run your driver locally, then:
```bash
csi-sanity --csi.endpoint=<driver-endpoint> \
  --csi.stagingdir=<staging-dir> --csi.mountdir=<mount-dir> \
  --csi.testvolumeparameters=params.yaml --csi.testvolumesize=1073741824 \
  --ginkgo.v
```
Documented and source-confirmed flags include `--csi.endpoint` (required), `--csi.controllerendpoint` (separate controller socket), `--csi.mountdir`, `--csi.stagingdir`, `--csi.createmountpathcmd`/`--csi.createstagingpathcmd`, `--csi.secrets` (YAML file with CreateVolumeSecret, NodeStageVolumeSecret and similar keys), `--csi.testvolumeaccesstype` (`mount` or `block`), `--csi.testvolumesize`, `--csi.testvolumeexpandsize`, `--csi.testvolumeparameters`, `--csi.testsnapshotparameters`, and `--version`. The full Ginkgo flags are available; `csi-sanity -h` lists them. It tests the Identity, Controller and Node RPCs against the CSI spec.

## External storage e2e: behaviour inside Kubernetes
`e2e.test` from Kubernetes (from the test tarball or `make WHAT=test/e2e/e2e.test`) accepts `-storage.testdriver=<file>` one or more times; the file is YAML or JSON defining the driver (see `driverDefinition` in external.go and the `Cap...` capability constants).
```yaml
StorageClass:
  FromName: true
SnapshotClass:
  FromName: true
DriverInfo:
  Name: my.csi.example.com
  Capabilities:
    persistence: true
    block: true
    exec: true
    snapshotDataSource: true
    controllerExpansion: true
    nodeExpansion: true
    topology: true
```
Unknown fields are silently ignored, so beware of typos. Run only these tests with the ginkgo CLI (from the README):
```bash
ginkgo -p -focus='External.Storage.*my.csi.example.com' \
       -skip='\[Feature:|\[Disruptive\]' \
       e2e.test -- -storage.testdriver=driver.yaml
```
Tests that depend on optional features are skipped this way and must be selected explicitly (for example `[Feature:VolumeSnapshotDataSource]`). Use an `e2e.test` that matches the cluster's Kubernetes version.

## Verify
csi-sanity passes, and the external e2e suite passes for every capability you declare.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: csi-sanity flags from main.go, storage.testdriver parameter, driver definition capabilities in testdriver.go, ginkgo invocation from the external e2e README.

Method: documentation only; no commands were run.
