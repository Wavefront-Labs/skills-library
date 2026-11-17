---
id: computing-software.cloud-infrastructure-engineering.kubespray.upgrade-across-kubespray-releases
name: upgrade-across-kubespray-releases
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [upgrade, releases, git-tags, minor-version, inventory]
level: sme
status: docs-checked
description: "Step through Kubespray release tags one at a time, never skipping minors, and re-check your inventory copy against the sample after each step."
sources:
  - https://kubespray.io/docs/operations/upgrades.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Do not skip minor releases when upgrading Kubespray; patch releases are fine. Upgrade by one tag at a time. The page's example: v2.22.0 to v2.23.2 to v2.24.0 is valid, v2.22.0 straight to v2.24.0 is not.

Procedure for each step:
1. `git checkout` the next tag.
2. Possibly `pip3 install -r requirements.txt` again (the page notes it may be needed).
3. Run `upgrade-cluster.yml` against your inventory.

If you do not set a Kubernetes version in `group_vars/k8s_cluster/k8s-cluster.yml`, checking out the next tag is enough. If you do define it, update it first or pass `-e kube_version=...`, otherwise the cluster stays at the version your inventory defines.

Review differences between the sample inventory and your own at every step. The page's worked example from v2.6.0 to v2.10.0 shows that variable formats in `k8s-cluster.yml` changed between 2.8.5 and 2.9.0, and that failing to keep your inventory copy current makes the upgrade fail and leaves the first master non-functional until fixed and re-run. It also notes that v2.10.0 appears between v2.1.2 and v2.2.0 in the `git tag` output.

## Checked

2026-11-04. The skip rule, procedure and warnings were confirmed on the Multiple upgrades section of the Upgrading page.

Method: documentation only; no commands were run.
