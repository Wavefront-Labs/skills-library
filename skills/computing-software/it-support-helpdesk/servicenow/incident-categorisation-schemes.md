---
id: computing-software.it-support-helpdesk.servicenow.incident-categorisation-schemes
name: incident-categorisation-schemes
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, incident-management, incident-categorization, category-subcategory, service-offering, configuration-item, itil-4, reporting-taxonomy]
level: practitioner
status: draft
description: "Design and apply incident categories that drive routing and reporting: service-based taxonomy, shallow trees, CI and service fields, 'Other' control, and recategorising at closure."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# incident-categorisation-schemes

Goal: categories that agents pick correctly in seconds and that produce
reports someone can act on (ITIL 4 incident management: logging and
categorisation).

## Design principles
- **Categorise by service/what's affected**, not by guessed cause: "Email",
  "VPN", "Laptop hardware", "Payroll app". Cause belongs in resolution
  codes.
- **Shallow**: 2 levels (category → subcategory), ~10–15 categories. Deep
  trees get "first plausible option" picks and garbage data.
- Use **Service / Service offering** and **Configuration item** fields
  (ServiceNow) for precision instead of more category levels; they also drive
  assignment and impact analysis.
- Mutually exclusive and named in users' words.
- An "Other" option only with a mandatory description, reviewed monthly to
  add missing categories.

## Example
| Category | Subcategories |
|---|---|
| Hardware | Laptop, Desktop, Monitor/peripheral, Mobile device, Printer |
| Account & access | Password/lockout, MFA, Access request (→ request, not incident) |
| Email & collaboration | Outlook, Teams, OneDrive/SharePoint |
| Network & remote access | Wi-Fi, VPN, Wired |
| Business application | (per major app) |
| Security | Phishing report, Malware, Lost/stolen device |

## Applying at logging
- Categorise from the **symptom as reported**; correct it when the real
  service is known.
- Recategorise at **resolution** — ServiceNow keeps the original in audit
  history; reports should use the final value (or both: "opened as" vs
  "resolved as" reveals misrouting).
- Requests (new access, new software) logged as incidents distort metrics —
  convert to a request.

## Using the data
- Top categories by volume and by time-to-resolve → problem candidates and
  shift-left targets.
- Category-to-assignment-group mapping (assignment rules) depends on the
  scheme being stable — change it through a controlled process.

## Gotchas
- Changing categories mid-year breaks trend reports — map old to new.
- Mandatory deep categorisation on the portal makes users pick randomly;
  keep portal forms simple, let agents refine.

## Verify
Monthly sample: ≥ 90 % of resolved incidents have a correct final category;
"Other" under 5 %; top-10 report produces at least one actionable problem
record.
