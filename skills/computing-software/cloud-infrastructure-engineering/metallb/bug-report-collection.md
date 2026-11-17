---
id: computing-software.cloud-infrastructure-engineering.metallb.bug-report-collection
name: bug-report-collection
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, bug-report, ephemeral-container, collect-sh, debug-logs, loglevel, distroless]
level: practitioner
status: docs-checked
description: "Prepare a useful MetalLB bug report: name the failing phase, set debug log level, run collect.sh, include Service and EndpointSlices, and debug distroless pods with kubectl debug."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bug report collection

State which phase fails. Good: "MetalLB is not replying to ARP requests", "the service IP is not advertised via BGP", "advertised only from a subset of nodes", "advertised but no traffic seen in tcpdump". Bad: "I can't curl the service", "MetalLB doesn't work".

Include:
1. Logs and YAML of all CRs, with log level debug:
   - Helm: `.controller.loglevel` and `.speaker.loglevel`
   - Operator: loglevel field in the MetalLB CRD
   - raw manifests: set the parameter on the speaker/controller containers manually
2. Collector script: https://raw.githubusercontent.com/metallb/metallb/main/troubleshooting/collect.sh
3. Service and endpoints:
```bash
kubectl get endpointslices <my-service> -o yaml
kubectl get svc <my_service> -o yaml
```

Debugging inside pods: the speaker and controller images are distroless, so use an ephemeral container:
```bash
kubectl debug -it -n metallb-system -c <ephemeral container name> --target=speaker --image=<ephemeral image name> <speaker pod>
```
The docs show only the speaker form of this command.

Before filing, go through `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-not-advertising` and `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-config-validation`.

## Checked
2026-11-04. Confirmed against the MetalLB Troubleshooting page, "Collecting information for a bug report": good and bad examples, loglevel fields, collect.sh URL, kubectl commands, distroless note and the kubectl debug command. Removed an unsupported controller-target instruction.
Method: documentation only; no commands were run.
