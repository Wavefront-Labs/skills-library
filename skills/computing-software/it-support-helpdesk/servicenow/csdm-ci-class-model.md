---
id: computing-software.it-support-helpdesk.servicenow.csdm-ci-class-model
name: csdm-ci-class-model
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, csdm, cmdb, ci-class, business-service, technical-service, service-offering, application-service]
level: advanced
status: gated
description: "Apply ServiceNow CSDM to support data: business vs technical services, service offerings, application services, CI classes, and which ones to put on incidents and changes."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/csdm-implementation/concept/csdm-implementation.html"
  - "https://www.servicenow.com/community/common-service-data-model/ct-p/common-service-data-model"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/configuration-management/concept/class-model.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# csdm-ci-class-model

The Common Service Data Model (CSDM, current version 5) is ServiceNow's prescribed shape
for the CMDB. Support teams feel it through the Service, Service offering and
Configuration item fields on tickets. Getting it right makes routing, impact and
reporting work.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Domains and the tables that matter to support
| Domain | Key classes (tables) | Support use |
|---|---|---|
| Design | Business application (`cmdb_ci_business_app`) | Ownership, portfolio; not put on tickets |
| Build/Manage technical services | Application service (`cmdb_ci_service_auto`), Technical service and offering (`cmdb_ci_service_technical`, `service_offering`) | What IT runs (e.g. "Email - Exchange Online"); assignment groups |
| Sell/Consume | Business service (`cmdb_ci_service_business`), Business service offering | What users consume ("Email - Standard"); SLAs, portal, impact |
| Foundation | Locations, groups, users, companies, product models | Routing, contacts |
| Infrastructure | Servers, computers, network gear (`cmdb_ci_computer`, `cmdb_ci_server`...) | The broken thing |

## On tickets
- **Service** (`business_service`): business service the user experiences.
- **Service offering**: tier/variant ("Email - EMEA"), drives SLA and support group.
- **Configuration item** (`cmdb_ci`): the specific failing CI (laptop, server, application
  service). Desk agents pick the user's device or the app service; resolvers refine.
- Changes: technical service offering or application service plus the infrastructure CIs
  touched, so impact analysis walks relationships upward.

## Practical rules
- Users never see technical services; portal categories map to business service offerings.
- Each offering needs a **support group** and **change group**; assignment lookup rules
  can use them instead of hand-built category routing.
- Don't create one service per application server; one application service per
  deployed environment (Prod, Test) with relationships to its servers.
- Start minimal ("crawl" stage): business applications, application services, technical
  service offerings, support groups. Add business services when SLAs require it.

## Gotchas
- Legacy `cmdb_ci_service` records used for everything (apps, teams, buildings) break CSDM
  reports; migrate them to the right classes with the CSDM data foundations dashboard.
- Reference qualifiers on the incident form must filter Service offering by the chosen
  Service, or agents pick random offerings.

## Verify
CSDM Data Foundations dashboard health checks pass for your stage; a sample of recent
incidents has service, offering and CI populated consistently with the model.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
