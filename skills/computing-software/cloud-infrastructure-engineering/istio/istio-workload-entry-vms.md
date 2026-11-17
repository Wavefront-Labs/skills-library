---
id: computing-software.cloud-infrastructure-engineering.istio.istio-workload-entry-vms
name: istio-workload-entry-vms
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, workloadentry, vm-workloads, workloadgroup]
level: practitioner
status: docs-checked
description: "Register VM workloads into the mesh with WorkloadGroup and WorkloadEntry, and understand that the VM needs a sidecar and network path to istiod."
sources: ["https://istio.io/latest/docs/setup/install/virtual-machine/", "https://istio.io/latest/docs/reference/config/networking/workload-group/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VMs join as mesh workloads. A `WorkloadGroup` is the template; each VM becomes a `WorkloadEntry`.

```yaml
apiVersion: networking.istio.io/v1
kind: WorkloadGroup
metadata: {name: legacy-app, namespace: shop}
spec:
  metadata: {labels: {app: legacy}}
  template: {serviceAccount: legacy, network: vm-network}
```

```sh
istioctl x workload entry configure -f workloadgroup.yaml -o vm-files --clusterID cluster1
```

The command generates `cluster.env` (namespace, service account, network CIDR and optional inbound ports), `istio-token` (a Kubernetes token used to get certificates from the CA) and `mesh.yaml` (ProxyConfig with the discovery address, health-checking probes and some authentication options). Copy the files to the VM and start the sidecar service (`sudo systemctl start istio`). Add `--autoregister` to have the WorkloadEntry created automatically.

Gotchas: VMs must have IP connectivity to the ingress gateway in the connecting mesh. Third-party tokens must be enabled in the cluster before generating `istio-token`; if not, add `--set values.global.jwtPolicy=first-party-jwt` to the Istio install commands. With automated WorkloadEntry creation, application health checks are available and share the API and behaviour of Kubernetes readiness probes.

Verify: `kubectl get workloadentry -n shop` lists the VM.

## Checked

2026-11-03. Confirmed in the Istio virtual machine installation guide: `WorkloadGroup` template with `serviceAccount` and `network`, `istioctl x workload entry configure -f ... -o ... --clusterID [--autoregister]`, the generated files, the third-party token note, connectivity requirement and health checks. Removed: the east-west port 15012 claim, the short-lived bootstrap token wording, the `proxy-status` check and the provisioning and service-account advice (not on the pages read).

Method: documentation only; no commands were run.
