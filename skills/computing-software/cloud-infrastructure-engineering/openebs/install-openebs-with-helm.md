---
id: computing-software.cloud-infrastructure-engineering.openebs.install-openebs-with-helm
name: install-openebs-with-helm
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [install, helm, openebs-chart, namespace, engines, rawfile, mayastor, crds]
level: practitioner
status: docs-checked
description: "Install OpenEBS with the openebs/openebs Helm chart, know the default engines, and use --set flags to drop Mayastor, enable Rawfile, skip snapshot CRDs or set kubelet dir."
sources:
  - https://openebs.io/docs/quickstart-guide/installation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Installation uses Helm 3.2 or later. Add the repo with `helm repo add openebs https://openebs.github.io/openebs`, refresh with `helm repo update`, then run:

```
helm install openebs --namespace openebs openebs/openebs --create-namespace
```

Defaults: this installs Local PV Hostpath, Local PV LVM, Local PV ZFS and Replicated Storage in the `openebs` namespace under the release name `openebs`. **Local PV Rawfile is not installed by default.** The page says the prerequisites must be met before installing.

Variations the page documents:

- Without Replicated Storage, add `--set engines.replicated.mayastor.enabled=false`.
- To include Rawfile, add `--set engines.local.rawfile.enabled=true`.
- If the CSI VolumeSnapshot CRDs already exist in the cluster, skip creating them with `--set openebs-crds.csi.volumeSnapshots.enabled=false`.

**Custom kubelet directory.** For a custom kubelet location, set it at install time with `--set`:

- Local PV LVM: `lvm-localpv.lvmNode.kubeletDir=<your-directory-path>`
- Local PV ZFS: `zfs-localpv.zfsNode.kubeletDir=<your-directory-path>`
- Replicated PV Mayastor: `mayastor.csi.node.kubeletDir=<your-directory-path>`

Named distributions: MicroK8s uses `/var/snap/microk8s/common/var/lib/kubelet/`, k0s uses `/var/lib/k0s/kubelet/`, and RancherOS uses `/opt/rke/var/lib/kubelet/` instead of the default `/var/lib/kubelet/`.

The full list of chart images is in the chart annotations: `helm show chart openebs/openebs | yq '.annotations."helm.sh/images"'`. Other configurable values are in the chart README in the openebs/openebs GitHub repository. Check the release with `helm ls -n openebs`; the sample output shows chart `openebs-4.6.0` with status `deployed`.

To validate the install, the page suggests provisioning a test volume with the `openebs-hostpath` StorageClass.

## Checked

Method: 2026-11-08 read the raw markdown of the cited installation page in full. Commands and flags match. Removed a reference to a separate kubelet-directory skill that the page does not make, replaced it with the kubelet paths the page lists, and dropped the unsupported claim that Hostpath needs no extra configuration.
