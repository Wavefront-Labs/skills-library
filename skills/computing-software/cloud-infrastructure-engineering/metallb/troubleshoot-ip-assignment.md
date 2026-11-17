---
id: computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-ip-assignment
name: troubleshoot-ip-assignment
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, ip-assignment, controller, pending, troubleshooting, speaker, events]
level: practitioner
status: docs-checked
description: "Diagnose a MetalLB Service stuck without an IP: controller vs speaker roles, and the checklist of pool selectors, dual-stack, requested IP and sharing conditions."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/usage/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting IP assignment

Roles: the `controller` assigns IPs; the `speaker`s announce them. No IP means look at the controller; IP assigned but unreachable means look at the speakers.

Check the controller log, and the Service events:
```bash
kubectl logs -n metallb-system deploy/controller
kubectl describe svc <name>
```
Things that block assignment (verify each):
- At least one `IPAddressPool` is compatible with the Service, including the selectors.
- A dual-stack Service needs a pool with both IPv4 and IPv6 addresses.
- If the Service asks for a specific IP, a pool providing it exists and its selectors permit the Service.
- If the IP is shared with other Services, they respect the sharing rules (same key, different ports, same policy or identical pods) in `computing-software.cloud-infrastructure-engineering.metallb.ip-sharing`.

Also: requesting (via `spec.loadBalancerIP` or the `metallb.io/loadBalancerIPs` annotation) an address MetalLB does not own, or one already used by another Service, makes assignment fail with a warning event visible in `kubectl describe service`.

Related: a stale config (`computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-config-validation`), and a full pool (`metallb_allocator_addresses_in_use_total` against `metallb_allocator_addresses_total`, the pair used by the sample exhausted-pool alert).

## Checked
2026-11-04. Confirmed against the MetalLB Troubleshooting page (controller versus speaker, assignment checklist) and the Usage page (specific IP requests, warning event, annotation, sharing conditions), plus the allocator metrics on the Prometheus Metrics page. Narrowed an unsupported "stays pending" claim about the address-pool annotation.
Method: documentation only; no commands were run.
