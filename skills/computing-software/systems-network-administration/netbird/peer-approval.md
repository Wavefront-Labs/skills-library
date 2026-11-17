---
id: computing-software.systems-network-administration.netbird.peer-approval
name: peer-approval
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, peer-approval, device-admission, pending-peers]
level: practitioner
status: docs-checked
description: "Require an administrator to approve each new NetBird device before it can reach network resources: availability, how to enable, approve and what happens on disable."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/approve-peers.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Peer approval makes an admin manually approve each device before it joins the network. Until approved, a device can reach the management service but has no access to other network resources.

Availability: NetBird Cloud Business plan, or self-hosted with an Enterprise Commercial License. Not in the open source Community Edition.

Enable: Settings > Authentication > turn on Peer approval.

Approve: Peers section > Approve button on the right of the peers table row.

Caution: disabling peer approval automatically approves all pending requests, so review the pending list first.

Approval can be automated with EDR integrations such as CrowdStrike, which approve trusted devices automatically.

## Checked

2026-11-04. Confirmed against the NetBird approve peers page: purpose, Business plan and Enterprise availability, Settings Authentication toggle, Approve button, auto-approval on disable, EDR automation. Removed the pointer to other skills and the user approval aside, which this page does not cover.
Method: documentation only; no commands were run.
