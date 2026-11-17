---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-platform-notes-gke-private-and-openshift
name: opa-gatekeeper-platform-notes-gke-private-and-openshift
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, gke, private-cluster, openshift, firewall, anyuid, net-bind-service]
level: advanced
status: docs-checked
description: "Make Gatekeeper work on private GKE clusters (port 8443 firewall or port 443) and OpenShift 4 (anyuid SCC) using the documented fixes."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/cloud-specific.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper platform notes gke private and openshift

Private GKE: master-to-node firewall rules allow only 443 and 10250. Gatekeeper exposes its service on 443, but GKE enables `--enable-aggregator-routing`, so the master bypasses the service and talks to the pod on 8443. Two fixes:
1. Add a firewall rule from the master to private nodes opening 8443 (or your custom port).
2. Run the pod on privileged port 443: set `--port=443`, `containerPort: 443`, and grant `NET_BIND_SERVICE` while dropping others:

```yaml
containers:
  - args: ["--port=443"]
    ports:
      - containerPort: 443
        name: webhook-server
        protocol: TCP
    securityContext:
      capabilities:
        drop: ["all"]
        add: ["NET_BIND_SERVICE"]
```

OpenShift 4.x: use the `anyuid` SecurityContextConstraint to keep a restricted profile while setting the user ID. Add a rule to the `gatekeeper-manager-role` Role:

```yaml
- apiGroups: ["security.openshift.io"]
  resourceNames: ["anyuid"]
  resources: ["securitycontextconstraints"]
  verbs: ["use"]
```

With this profile the `container.seccomp.security.alpha.kubernetes.io/manager: runtime/default` annotation cannot be set; given the few privileges anyuid grants, remove the annotation.

## Checked

2026-11-08. Confirmed against cloud-specific.md, read in full: private GKE ports and aggregator routing, both workarounds and the manifest snippet, OpenShift anyuid SCC role rule and the seccomp annotation note. Removed or corrected: nothing.

Method: documentation only; no commands were run.
