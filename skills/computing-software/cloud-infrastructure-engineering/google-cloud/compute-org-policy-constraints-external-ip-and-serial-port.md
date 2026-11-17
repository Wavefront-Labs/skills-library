---
id: computing-software.cloud-infrastructure-engineering.google-cloud.compute-org-policy-constraints-external-ip-and-serial-port
name: compute-org-policy-constraints-external-ip-and-serial-port
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, org-policy, compute-constraints, vm-external-ip-access, vmexternalipaccess, serial-port, os-login, shielded-vm, compute-engine]
level: practitioner
status: docs-checked
description: "Apply the Compute Engine org policy baseline: no external IPs, no serial port, OS Login, Shielded VM, no default network, no IP forwarding, with allowlists for exceptions."
sources: ["https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address#disableexternalip", "https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints", "https://cloud.google.com/compute/docs/troubleshooting/troubleshooting-using-serial-console"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute constraints: external IP, serial port and the VM baseline

## 1. The baseline set
| Constraint | Type | Baseline |
|---|---|---|
| `compute.vmExternalIpAccess` | list (instance paths) | deny all; allowlist named instances |
| `compute.disableSerialPortAccess` | boolean | enforce |
| `compute.disableSerialPortLogging` | boolean | enforce where logs could hold secrets |
| `compute.requireOsLogin` | boolean | enforce |
| `compute.requireShieldedVm` | boolean | enforce |
| `compute.skipDefaultNetworkCreation` | boolean | enforce |
| `compute.vmCanIpForward` | list | deny all; allow NVAs only |
| `compute.disableNestedVirtualization` | boolean | enforce unless needed |
| `compute.restrictProtocolForwardingCreationForTypes` | list | restrict to the forwarding types you need |

All of the constraints above appear on the Organization policy constraints reference page (gcloud has no `org-policies list-constraints` command). The page also lists
newer `compute.managed.*` constraints such as `compute.managed.disableNestedVirtualization` and `compute.managed.blockProjectSshKeys`; check whether a managed equivalent exists before choosing. The "Baseline" column is a suggested starting point, not Google's default.

## 2. External IP: deny with an allowlist
```yaml
name: organizations/<ORG_ID>/policies/compute.vmExternalIpAccess
spec:
  rules:
  - values:
      allowedValues:
      - projects/edge-prod/zones/europe-west2-a/instances/bastion-legacy
```
Allowed values are full instance paths (`projects/PROJECT_ID/zones/ZONE/instances/INSTANCE`); the constraints page also describes a deny-all form.

## 3. Serial port
`compute.disableSerialPortAccess` blocks the interactive serial console
(`serial-port-enable=TRUE` metadata is ignored). For break-glass debugging, override it on a
single project with a time-boxed policy and remove it afterwards:
```bash
cat > sp.yaml <<'EOF'
name: projects/<P>/policies/compute.disableSerialPortAccess
spec: {rules: [{enforce: false}]}
EOF
gcloud org-policies set-policy sp.yaml   # remember: gcloud org-policies delete afterwards
```

## Gotchas
- The constraints page says enforcement of these constraints is not retroactive for existing resources; audit existing VMs separately.
- Services that create VMs on your behalf (for example GKE) are subject to the same constraints; check their private-networking options before enforcing.

## Verify
- [ ] Creating a test VM with an external IP in an enforced project fails with an organisation-policy constraint violation.
- [ ] A serial port connection is refused on an enforced project.
- [ ] `gcloud org-policies describe <constraint> --project=<P> --effective` shows the expected value for each row above.

## Checked

- Date: 2026-10-27
- Confirmed against the Organization policy constraints list (all nine constraint names in the table exist: `compute.vmExternalIpAccess`, `compute.disableSerialPortAccess`, `compute.disableSerialPortLogging`, `compute.requireOsLogin`, `compute.requireShieldedVm`, `compute.skipDefaultNetworkCreation`, `compute.vmCanIpForward`, `compute.disableNestedVirtualization`, `compute.restrictProtocolForwardingCreationForTypes`; instance path format; serial port access ignores metadata attributes) and the gcloud `org-policies set-policy` and `delete` references.
- Removed: `gcloud org-policies list-constraints` (no such command), the `is:INTERNAL` value, managed-constraint dry-run claim, MIG/NAT advice, instance list filter, GKE/Dataproc/Composer notes, OS Login metadata claim and the exact violation message.

Method: documentation only; no commands were run.
