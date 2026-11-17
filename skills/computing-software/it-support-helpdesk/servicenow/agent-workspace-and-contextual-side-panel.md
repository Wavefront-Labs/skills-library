---
id: computing-software.it-support-helpdesk.servicenow.agent-workspace-and-contextual-side-panel
name: agent-workspace-and-contextual-side-panel
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, agent-workspace, service-operations-workspace, contextual-side-panel, agent-assist, ux-framework, list-views]
level: practitioner
status: gated
description: "Work in ServiceNow Agent / Service Operations Workspace: lists and tabs, contextual side panel (CI, user, KB agent assist), playbooks, and workspace vs classic UI pitfalls."
sources:
  - "https://www.servicenow.com/docs/bundle/xanadu-it-service-management/page/product/service-operations-workspace/concept/service-operations-workspace.html"
  - "https://www.servicenow.com/docs/bundle/xanadu-platform-user-interface/page/administer/workspace/concept/contextual-side-panel.html"
  - "https://www.servicenow.com/docs/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# agent-workspace-and-contextual-side-panel

ServiceNow's agent UIs are workspaces built on Next Experience (Service Operations
Workspace for ITSM; older instances use Agent Workspace). They replace the classic form
for desk agents.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Layout
| Area | Use |
|---|---|
| Left nav (Lists) | Saved lists: My work, Unassigned, My group, Major incidents |
| Record tabs | Several records open as tabs; stays in one browser tab |
| Record header | Priority, state, SLA timers |
| Activity stream | Work notes vs additional comments (customer-visible) with compose box |
| Contextual side panel | Caller details, related records, CI, Agent Assist, attachments |

## Contextual side panel
- **Caller / requester**: recent tickets, VIP flag, location, assets. Check before replying;
  repeat callers often have a parent incident already.
- **Agent Assist**: searches knowledge, similar incidents and catalog items from the
  short description; attach an article with one click (links it and can paste the link as
  a comment). This feeds KCS reuse metrics.
- **CI / affected services**: open problems and changes on the CI; a matching active
  change is the fastest diagnosis.
- **Playbooks** (process guidance): step cards for major incident or request types.

## Agent habits that matter
1. Use **work notes** for internal detail, **additional comments** for the user; the
   compose box toggle is easy to miss.
2. Create child/related records from the side panel so relationships are recorded.
3. Use list filters and save them as personal lists rather than exporting to Excel.
4. Use templates/quick messages (see servicenow-record-templates-and-quick-messages).

## Admin notes
- Lists, side panel sections and form layouts are configured in UI Builder / Workspace
  admin, separate from classic form layouts; a field added to the classic form does not
  appear in the workspace automatically.
- UI policies and client scripts must be set to run on "All" UI types or
  workspace-specific variants; classic-only scripts silently do nothing in the workspace.

## Gotchas
- Some legacy UI actions (buttons) are hidden in workspace unless flagged "Workspace form
  button".
- Browser zoom and many tabs slow the workspace; close tabs at shift end.

## Verify
Open an incident in the workspace, confirm the side panel shows caller history and
Agent Assist results, attach a KB, add a work note and a comment, and check the user
sees only the comment.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
