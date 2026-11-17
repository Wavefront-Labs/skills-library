---
id: computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-config-validation
name: troubleshoot-config-validation
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, config-validation, webhook, stale-config, troubleshooting, logs, controller, speaker]
level: practitioner
status: docs-checked
description: "Check whether MetalLB rejected your configuration: validation webhooks only catch some errors, bad configs are marked stale, and where to look in logs and metrics."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration validity

MetalLB ships validation webhooks for the CRs, but the configuration is the composition of many resources (IPAddressPools, L2Advertisements, BGPAdvertisements...), validated as a whole. Not all invalid combinations are blocked at apply time.

Behaviour: an invalid configuration is marked stale and MetalLB keeps working with the last valid one. Each component validates the part relevant to it, so the controller may accept a config the speaker rejects.

Today the reason is surfaced only in the controller/speaker logs (the docs say future releases will expose it in Kubernetes resources).

Check:
1. Logs of each component: errors look like `failed to parse the configuration` plus detail.
```bash
kubectl logs -n metallb-system deploy/controller
kubectl logs -n metallb-system ds/speaker
```
2. Prometheus: `metallb_k8s_client_config_stale_bool` equals 1 on the affected component (`computing-software.cloud-infrastructure-engineering.metallb.alert-rules`).

Gotcha: an `invalid configuration` log line does not necessarily mean the last loaded config is invalid.

For pool removal with IPs in use see `computing-software.cloud-infrastructure-engineering.metallb.stale-config-changing-service-ip`.

## Checked
2026-11-04. Confirmed against the MetalLB Troubleshooting page ("Valid Configuration") and the Configuration page ("Configuration validation"): webhooks, whole-configuration validation, stale marking, log text, stale metric, the invalid-configuration-log caveat. The metric also appears on the Prometheus Metrics page. Removed an unsupported fix-and-confirm step.
Method: documentation only; no commands were run.
