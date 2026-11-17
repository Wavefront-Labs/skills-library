---
id: computing-software.systems-network-administration.network-design.network-change-management
name: network-change-management
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, change-management, itil, change-advisory-board, rollback-plan, maintenance-window, mop, peer-review]
level: practitioner
status: docs-checked
description: "Run network changes through a disciplined process: change classes, method of procedure with pre/post checks and rollback, peer review, windows and post-change verification."
sources:
  - https://sre.google/sre-book/introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network change management

Google's SRE book notes that most outages are caused by some kind of change (a new configuration, a new feature launch, or new user traffic). Process is the cheapest redundancy.

## Change classes (common practice)
| Class | Example | Approval |
|---|---|---|
| Standard | pre-approved, low risk, scripted: add VLAN to access port, update a description | none per change, template reviewed once |
| Normal | routing policy change, firmware upgrade, new firewall rules | peer review + CAB/approver, scheduled window |
| Emergency | fix an active outage | approve fast, document after, review in CAB |

## Method of procedure (MOP)
1. **Purpose and impact:** what changes, which services/sites, expected interruption.
2. **Pre-checks:** capture the state you will compare: route table summary, BGP prefix counts,
   interface states, a configuration backup, a monitoring screenshot.
3. **Implementation steps:** exact commands per device, in order. Use a safety net for remote changes
   (timed reload, configuration replace or rollback, or a commit-confirmed style feature where the
   platform has one).
4. **Post-checks:** same commands as pre-checks plus service tests (app owner confirms).
5. **Rollback plan:** exact commands, the trigger (a measurable threshold, such as an expected prefix
   count after a set wait) and the decision deadline inside the window.
6. **Communication:** who is told before/after, war-room channel.

## Practices
- Peer review the config diff, not a description of it. Git + pull requests for config templates.
- One logical change per window; do not bundle "while we are in there".
- Freeze periods (quarter end, retail peaks).
- Automated pre/post diffs beat eyeballing.
- Post-incident review for every failed change; update the MOP template.

## Verify
- [ ] Every normal change has an approved MOP with pre/post evidence attached and rollback tested or rehearsed; change success rate tracked.

## Checked

2026-10-28: Confirmed in the SRE book introduction: outages are mostly caused by changes (a new configuration, a new feature launch, or a new type of user traffic). The ITIL page returned nothing and the Cisco change-management URL is a 404, so both sources were removed and the change classes are labelled common practice, not ITIL text. Removed: the 5 min rollback example, the Cisco command names, reload in 10, and the Batfish/pyATS/Nornir tool names.
Method: documentation only; no commands were run.
