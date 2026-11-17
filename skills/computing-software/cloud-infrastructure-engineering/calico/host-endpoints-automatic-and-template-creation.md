---
id: computing-software.cloud-infrastructure-engineering.calico.host-endpoints-automatic-and-template-creation
name: host-endpoints-automatic-and-template-creation
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [host-endpoint, kubecontrollersconfiguration, auto-hep, templates, nodeselector, kubernetes-nodes, labels]
level: practitioner
status: docs-checked
description: "Have calico-kube-controllers create wildcard host endpoints for every node, or template host endpoints by node selector and interface CIDR, then target them with node labels."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/hosts/kubernetes-nodes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Automatic host endpoints use `interfaceName: "*"`, covering all interfaces in the host network namespace. Calico creates one per node with the node's labels and IPs, re-syncs them periodically, and marks them with the label `projectcalico.org/created-by: calico-kube-controllers`.

**Enable:**

```bash
calicoctl patch kubecontrollersconfiguration default --patch='{"spec": {"controllers": {"node": {"hostEndpoint": {"autoCreate": "Enabled"}}}}}'
```

Check with `calicoctl get heps -owide`; the profile shown is `projectcalico-default-allow`.

**Templates** fine-tune which nodes and interfaces get endpoints. Set under `spec.controllers.node.hostEndpoint.templates`:

```yaml
spec:
  controllers:
    node:
      hostEndpoint:
        autoCreate: Enabled
        createDefaultHostEndpoint: Disabled
        templates:
          - generateName: custom-host-endpoint
            interfaceCIDRs:
              - 192.168.0.0/16
            nodeSelector: "!has(node-role.kubernetes.io/control-plane)"
            labels:
              custom-label: template-host-endpoint
```

Apply with `kubectl patch kubecontrollersconfiguration default --patch-file hostEndpointTemplate.yaml --type merge`. The page's sample output still shows `createDefaultHostEndpoint: Enabled` after the patch, so check the live resource.

**Targeting.** Label nodes and the label syncs to their host endpoints: `kubectl label nodes --all kubernetes-host=`, then select with `has(kubernetes-host)`, or combine as `has(kubernetes-host) && environment == 'dev'`.

## Checked

2026-11-08. The Protect Kubernetes nodes page was read in full. Enable command, template YAML, label and sync behaviour and selector examples were confirmed on the Protect Kubernetes nodes page.

Method: documentation only; no commands were run.
