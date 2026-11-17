---
id: computing-software.cloud-infrastructure-engineering.rook.rook-openshift-scc-and-settings
name: rook-openshift-scc-and-settings
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [openshift, securitycontextconstraints, operator-openshift, hostpath-requires-privileged, oc]
level: practitioner
status: docs-checked
description: "Deploy Rook on OpenShift with its security context constraints, the privileged hostPath setting and an object store port above 1023."
sources:
  - https://rook.io/docs/rook/latest-release/Getting-Started/ceph-openshift/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OpenShift security context constraints must allow the Rook pods to run. Rook needs to create hostPath volumes for mons and OSDs, run privileged pods for access to `/dev`, use host networking where required, and give OSDs host PIDs.

Example files in `deploy/examples`:
- `operator-openshift.yaml` creates the SCCs and starts the operator
- `object-openshift.yaml` creates an object store with RGW on a valid port

Commands:
```
oc create -f crds.yaml -f common.yaml
oc create -f operator-openshift.yaml
oc create -f cluster.yaml
```
Creating the SCC needs a privileged account (`oc login -u system:admin`). If Rook runs in a namespace other than `rook-ceph`, edit the example SCC for your namespaces. Older OpenShift versions may need `apiVersion: v1`.

Operator setting: `ROOK_HOSTPATH_REQUIRES_PRIVILEGED` must be `"true"`. With SELinux restrictions the pod must be privileged to write to the hostPath volume, which the mon, OSD and CSI provisioner pods (when log rotation is on) need.

In the cluster CR, make sure `dataDirHostPath` is a valid writable host path. In the object store CRD, ports below 1024 cannot be bound on OpenShift, so use `gateway.port: 8080`; a service can expose a different port such as 80.

The Helm charts create the SecurityContextConstraints automatically.

## Checked

2026-11-03. Confirmed against the OpenShift page: the example files, the oc commands, ROOK_HOSTPATH_REQUIRES_PRIVILEGED, dataDirHostPath and the object store port 8080. Removed: nothing.

Method: documentation only; no commands were run.
