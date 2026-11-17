---
id: computing-software.it-support-helpdesk.servicenow.vip-and-executive-support-model
name: vip-and-executive-support-model
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, vip-executive-support, vip-flag, executive-assistants, white-glove, service-desk, priority-handling]
level: practitioner
status: draft
description: "Design and run VIP/executive support: who qualifies, the VIP flag and routing in ServiceNow, delegate and assistant handling, travel prep, and limits so priority isn't abused."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/users-and-groups/reference/r_UserFormFields.html"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-service-desk"
  - "https://www.thinkhdi.com/library/supportworld/2016/supporting-vips"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vip-and-executive-support-model

Every desk has VIP support, formally or informally. Formal is better: clear scope,
named people, and the rest of the desk isn't disrupted by unofficial "the CEO's PA rang".

## Scope
- Who: a named list (executive team, board, their assistants), reviewed quarterly with HR
  or the chief of staff. Not "all directors".
- What: faster response, a named engineer, desk-side or remote first, proactive device
  care, travel and meeting-room readiness. Not: bypassing security controls, approval
  steps or change management.

## ServiceNow setup
- User record `vip = true` (base field). Base form shows a VIP icon next to the caller.
- Routing: assignment rule or AWA queue condition `caller_id.vip=true` sends to a VIP
  queue/group; or keep normal group with a notification to the VIP engineer.
- Priority: don't auto-raise priority for VIPs (it breaks impact/urgency logic and
  reports). Use a separate response OLA for VIP tickets instead, measured with its own SLA
  definition (`caller_id.vip=true`).
- Assistants: record delegates (Delegates related list) so tickets raised by an assistant
  on behalf of the exec show both people; set caller = the exec, opened by = assistant.

## Service practices
- Named primary and backup engineer; executives' devices on the newest standard build.
- Before travel: check device updates, VPN, roaming/eSIM, chargers, MFA on a second
  device, offline copies of key files.
- Board meetings: room and video checks 30 minutes before, engineer on standby.
- Device swaps prepared in advance (pre-built spare, data on OneDrive) so a failure is a
  15-minute swap.
- Discretion: executives' tickets can contain sensitive matters; restrict visibility with
  a data policy/ACL on VIP tickets if needed.

## Limits
- Security exceptions requested by executives go through the normal risk acceptance
  process. Executives are the most targeted users (whaling, MFA fatigue).
- Track VIP volume; if VIP tickets grow fast, the list or the underlying service quality
  needs review.

## Gotchas
- Only one engineer knows the execs' setups: document everything in the CMDB and KB.
- Assistants raising issues by personal message to engineers: still log a ticket.

## Verify
VIP list current, VIP tickets route and meet their OLA, delegates recorded, and a quarterly
review with the executive office is held.
