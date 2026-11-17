---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-center-of-excellence
name: cloud-center-of-excellence
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, cloud-center-of-excellence, ccoe, cloud-adoption-framework, enablement]
level: practitioner
status: docs-checked
description: "Stand up a cloud centre of excellence: function structure, objectives, negotiation with existing IT, and the stakeholder support it needs."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/organize/cloud-center-of-excellence"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud centre of excellence (CCoE)

From the Cloud Adoption Framework CCoE article. Note: Microsoft marks the article deprecated, no longer updated, and
due for removal on 30 November 2026, so treat it as dated guidance. A CCoE is a function that helps organisations
balance speed and stability while pursuing business and technical agility.

## Function structure
A CCoE model needs collaboration between cloud adoption (solution architects), cloud strategy (program and project
managers), cloud governance, cloud platform and cloud automation.

## Objectives
Accelerate cloud adoption through cloud-native or hybrid solutions: build a modern IT organisation using agile
approaches, provide reusable deployment packages aligned with security, compliance and management policies,
maintain a functional Azure platform per operational procedures, review and approve cloud-native tools, and
standardise and automate common platform components over time.

## Effect on IT
IT shifts from operations unit or control point (the stoplight analogy) toward broker and partner, with delegated
responsibility (the roundabout analogy). The article calls both approaches valid; a CCoE fits where you want a
self-service model in which business units decide within guidelines and repeatable controls.

## Operating notes
- Maximise natural interaction, minimise meetings; track growth through a common repository or solution catalog.
  A meeting after each release plan is shared gives a minimum touch point.
- Negotiation with existing IT is at the root of CCoE work: IT gives up manual approval control, change control
  stability and similar comforts in exchange for automation of common issues, consistency, fewer high-severity
  incidents, learning opportunities and a broader technical scope.

## Stakeholder support
- Needs the CIO and executive IT leadership, plus business stakeholders (line-of-business, finance, operations,
  product owners), since agility and time to market motivate the CCoE.
- Document expected business outcomes, current IT pain points and their historical effects, blocked improvement
  opportunities, and timelines and metrics.
- For the first six to nine months the article recommends monthly meetings of business stakeholders, IT leadership
  and the CCoE, and keeping business stakeholders informed of progress and blockers.
- IT stakeholders should support the vision (and break deadlocks if needed), maintain focus (protect CCoE time
  from day-to-day disruption) and create a buffer for "fast-fail" experiments while holding the team to a growth
  mindset.

## Verify
- [ ] The five functions have named owners and a sponsor from IT leadership.
- [ ] Business stakeholder cadence is scheduled.

## Checked
2026-11-09. Confirmed against the Cloud Adoption Framework CCoE article (downloaded HTML; function structure,
effects, responsibilities, negotiation and stakeholder sections read). Removed unconfirmed claims and the AWS
whitepaper source (not read): team size of 4-8, named roles such as FinOps and security engineer, the service
catalogue, metrics list (NPS, provisioning time) and the plan to shrink the CCoE into platform and FinOps teams.
Method: docs-checked 2026-11-09 against learn.microsoft.com/azure/cloud-adoption-framework/organize/cloud-center-of-excellence downloaded HTML; documentation only, no commands run.
