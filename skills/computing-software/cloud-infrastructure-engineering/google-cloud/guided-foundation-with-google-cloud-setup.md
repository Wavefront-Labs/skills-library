---
id: computing-software.cloud-infrastructure-engineering.google-cloud.guided-foundation-with-google-cloud-setup
name: guided-foundation-with-google-cloud-setup
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, landing-zone, google-cloud-setup, guided-foundation-setup, foundation-setup-checklist, terraform-download]
level: practitioner
status: docs-checked
description: "Choose and run a Google Cloud Setup foundation option (proof of concept, production, advanced production) and know what each includes."
sources: ["https://cloud.google.com/docs/enterprise/cloud-setup", "https://cloud.google.com/docs/enterprise/setup-checklist"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guided foundation with Google Cloud Setup

Google Cloud Setup is the interactive guide in the console that Google recommends administrators run before running
workloads on Google Cloud. You can deploy its default configuration or adjust it to your business needs.

## What a foundation includes
- A folder configured for application management.
- A management project for access, billing, observability and other administrative functions of your applications.
- A standard project where you can deploy resources.
- Administrator groups required to configure each foundation option.
- Recommended organisation policies.

## Pick an option
| Option | Use when | Scope |
|---|---|---|
| Proof of concept | Experimenting before a larger commitment | Organization, Billing and Resource Hierarchy tasks |
| Production | Production-ready workloads, security and scalability | Everything in proof of concept plus logging, monitoring and Security Command Center settings |
| Advanced production | Highly secure or complex workloads, strict security requirements | Everything in production plus networking settings and Cloud KMS with Autokey configuration |

Start from the Foundations page of Google Cloud Setup, click Start under the chosen option, then follow that option's
own page (Create a proof of concept / production / advanced production foundation).

## Gotchas
- It is a starting point for a single foundation. For a multi-team landing zone with pipelines use Fabric FAST or the
  terraform-example-foundation skills in this folder.
- Console changes made after deployment are not tracked in code; if you manage the foundation in Terraform, make changes
  there to avoid drift.

## Verify
- [ ] The folder, management project, standard project and admin groups exist as planned for the chosen option.

## Checked
2026-11-09: confirmed the foundation contents and the three options from the Google Cloud Setup guided flow page (the
setup-checklist URL redirects to the same page). Removed unconfirmed specifics: the numbered step list, folder names,
Shared VPC/NAT details, Terraform download, Organization Administrator requirement and the console URL (sign-in page).
Method: documentation only; no commands were run.
