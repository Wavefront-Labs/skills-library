---
id: computing-software.it-support-helpdesk.servicenow.handing-security-incidents-to-secops
name: handing-security-incidents-to-secops
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, security-incident-handoff, security-incident-response, csirt, incident-management, evidence-preservation]
level: practitioner
status: draft
description: "Recognise when a service desk ticket is really a security incident and hand it to SecOps or the CSIRT cleanly: triggers, what to capture, what not to touch, and ticket linkage."
sources:
  - "https://csrc.nist.gov/pubs/sp/800/61/r3/final"
  - "https://www.servicenow.com/docs/bundle/zurich-security-management/page/product/security-incident-response/concept/c_SecurityIncidentResponse.html"
  - "https://www.cisa.gov/topics/cyber-threats-and-advisories/incident-detection-response"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# handing-security-incidents-to-secops

The service desk is often first to hear about a security incident, usually disguised as
"my PC is acting weird". The job is to recognise it, preserve what matters and hand it to
the people who own response, without trying to investigate it yourself.

## Triggers that mean "hand off now"
- User clicked a link and entered credentials, or approved an unexpected MFA prompt.
- Ransom note, files renamed with odd extensions, mass file changes in OneDrive.
- EDR or antivirus alert the user reports, or a disabled security tool.
- Unknown remote access tool running, or someone called pretending to be IT.
- Lost or stolen device holding company data.
- Mail rules forwarding externally that the user didn't create.
- Data sent to the wrong recipient (also a privacy matter).

## Capture before handing off
- Who, what, when: user, device name, time first noticed, what they saw (exact text or a
  photo of the screen), what they already did ("I restarted it").
- Indicators: sender address, URL (defanged: `hxxps://example[.]com`), file names.
- Whether the device is still on the network.

## Do and don't
- **Do** follow the runbook for containment the desk is allowed to do: disconnect from
  network (Wi-Fi off / unplug, leave powered on), reset password and revoke sessions if
  credentials were entered, isolate via EDR if your role permits.
- **Don't** power off (loses memory evidence), run cleanup tools, delete the email, or
  reimage. Don't forward the malicious email as an attachment to colleagues.
- Don't discuss details on public channels or with the wider team.

## Ticket mechanics
- In ServiceNow with Security Incident Response: create a **security incident** from the
  incident (Create Security Incident related link) so the original is linked; restrict
  the original's work notes from then on.
- Without SIR: assign to the security queue and phone the on-call security contact for
  anything active (ransomware, compromised admin). A queue alone is not a handoff.
- Keep the original incident open for the user's productivity issue (loaner, password),
  but reference the security record rather than copying details into it.

## Verify
Security confirms receipt (named person), the security record links the original ticket,
and the user knows who will contact them next.
