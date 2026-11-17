---
id: computing-software.it-support-helpdesk.user-support-communication.sops-runbooks-network-diagrams-and-escalation-templates
name: sops-runbooks-network-diagrams-and-escalation-templates
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, standard-operating-procedure, runbook, network-diagram, escalation-template, documentation, support-documentation]
level: practitioner
status: draft
description: "Write support docs that get used: SOPs for repeatable work, runbooks for operations and alerts, network diagrams for support, and escalation templates with required info."
sources:
  - "https://learn.microsoft.com/en-us/style-guide/welcome/"
  - "https://sre.google/sre-book/being-on-call/"
  - "https://www.thinkhdi.com/certification/support-center-analyst"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sops-runbooks-network-diagrams-and-escalation-templates

## SOP vs runbook vs KB article
| Document | Answers | Example |
|---|---|---|
| SOP | How we always do this process, with approvals and records | New starter account creation, laptop disposal |
| Runbook | What to do when this alert/event happens, step by step | "Backup job failed" alert, "VPN gateway down" |
| KB article | How to fix this symptom for a user | "Outlook keeps asking for password" |

## SOP template
Title, purpose, scope, owner, version and review date; roles; prerequisites; numbered
steps (one action each, with expected result); records to keep; exceptions and who
approves them; related documents. Review annually or when the process changes.

## Runbook template
- Trigger (alert name or symptom), impact, severity.
- Quick checks with exact commands and expected output.
- Remediation steps, in order of least risk; when to stop and escalate (and to whom,
  with on-call contact method).
- Verification, communication (who to notify), and links to dashboards.
- Keep runbooks next to the alert (link in the alert text) so on-call finds them in
  seconds. Update after every incident where the runbook was wrong.

## Network diagrams for support
- Support needs **logical** diagrams: sites, internet links, firewalls, VPN gateways,
  key VLANs and subnets, DNS/DHCP servers, where Wi-Fi controllers live, and which
  provider owns each link (with circuit IDs and support numbers).
- Physical diagrams (rack, patch panel, switch port maps) for site staff.
- Tools: Visio, draw.io/diagrams.net; store in the KB with a date and owner; update with
  every network change (change record checklist item).
- Don't publish diagrams with credentials or full firewall rules to a broad audience.

## Escalation templates
Before escalating to L2/L3 or a vendor, the ticket must contain:
- Symptom and impact (users affected, business process blocked), priority reason.
- Environment: user, device name, OS/build, app version, location/network (office, VPN).
- When it started and what changed; reproducible steps; error text or screenshot.
- What you tried and the results; relevant log snippets or bundle attached.
- What you need from the next team (a specific question or action).
Put this as a template (quick message / macro) and reject escalations missing it kindly
but consistently.

## Verify
Each recurring process has an SOP with a current review date, alerts link to runbooks,
diagrams are dated within the last change cycle, and escalations pass the template check.
