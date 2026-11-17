---
id: computing-software.cloud-infrastructure-engineering.google-cloud.architecture-framework-sustainability-practices
name: architecture-framework-sustainability-practices
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sustainability, sustainability-pillar, architecture-framework, energy-efficiency, rightsizing, design-review]
level: practitioner
status: docs-checked
description: "Apply the Google Cloud Well-Architected Framework sustainability pillar in design reviews: regions, resource usage, software, data, and measurement."
sources: ["https://cloud.google.com/architecture/framework/sustainability", "https://cloud.google.com/architecture/framework"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Architecture Framework sustainability practices

Use as a checklist in design reviews alongside cost and reliability. The framework's sustainability pillar maps its
recommendations to eight core principles; use them as the review headings.

## Core principles as review questions
| Principle | Question to ask |
|---|---|
| Use regions that consume low-carbon energy | Is the region a low-carbon one that still meets latency and residency needs? |
| Optimize AI and ML workloads for energy efficiency | Is specialised hardware (GPUs, TPUs) and an efficient algorithm used for the ML job? |
| Optimize resource usage for sustainability | Are VMs right-sized, autoscaling aggressive, idle resources removed, serverless services that scale to zero considered? |
| Develop energy-efficient software | Are hot paths efficient, so tasks finish faster and use fewer kWh? |
| Optimize data and storage for sustainability | Is old data archived or deleted, and is stored data kept to what is needed? |
| Continuously measure and improve sustainability | Are emissions measured and owned? |
| Promote a culture of sustainability | Is there a named owner and a review habit? |
| Align sustainability practices with industry guidelines | Which external guideline does the design follow? |

## Review output
For each workload: chosen region and the reason, utilisation targets, idle-cleanup automation, measurement owner.

## Gotchas
- The pillar frames cost and sustainability as mostly aligned (right-sizing, autoscaling, archiving and removing idle
  resources cut both), but check each decision explicitly rather than assuming.
- Shared responsibility applies: Google is responsible for the sustainability of Google Cloud (data centres,
  infrastructure, core services); you are responsible for optimising your workloads.
- Do not trade reliability targets away silently; document trade-offs. The pillar notes security incidents (DoS, breach
  recovery) also drive resource spikes, so security and resilience support sustainability.

## Verify
- [ ] Design doc contains a sustainability section with a measured baseline and planned improvements.

## Checked
2026-11-09: confirmed against the Well-Architected Framework sustainability pillar page (core principles list, cost
and right-sizing/autoscaling/archiving wording, shared responsibility, security-and-resilience section). Removed
unconfirmed specifics: machine-family names, Cloud Profiler, CFE percentages, Active Assist category claim, and the
reduce-carbon-footprint source (404).
Method: documentation only; no commands were run.
