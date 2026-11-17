---
id: computing-software.cloud-infrastructure-engineering.velero.fs-backup-platform-hostpaths
name: fs-backup-platform-hostpaths
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [node-agent-daemonset, hostpath, openshift, privileged-node-agent, rancheros]
level: advanced
status: docs-checked
description: "Adjust the node-agent DaemonSet kubelet hostPath or privileges for RancherOS, Nutanix, OpenShift and Tanzu so FSB can read pod volumes."
sources:
  - https://velero.io/docs/main/file-system-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some Kubernetes platforms need the node-agent DaemonSet changed after install. The default pod volume hostPath is `/var/lib/kubelet/pods`.

- RancherOS: change the hostPath to `/opt/rke/var/lib/kubelet/pods`.
- Nutanix: change it to `/var/nutanix/var/lib/kubelet`.
- VMware Tanzu Kubernetes Grid Integrated Edition: enable `Allow Privileged` in the plan and change it to `/var/vcap/data/kubelet/pods`.
- OpenShift: run node-agent privileged.

```
oc adm policy add-scc-to-user privileged -z velero -n velero
velero install --use-node-agent --privileged-node-agent
```

Without privilege, SELinux blocks access to pod volumes in the mounted hostPath. As an alternative you can create a custom SCC that allows hostPath without granting the `privileged` SCC.

OpenShift also needs the Velero namespace to schedule on all nodes. Annotate it before installing:

```
oc annotate namespace <velero namespace> openshift.io/node-selector=""
```

or export the DaemonSet, annotate the namespace, and recreate it:

```
oc get ds node-agent -o yaml -n <velero namespace> > ds.yaml
oc annotate namespace <velero namespace> openshift.io/node-selector=""
oc create -n <velero namespace> -f ds.yaml
```

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/file-system-backup/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
