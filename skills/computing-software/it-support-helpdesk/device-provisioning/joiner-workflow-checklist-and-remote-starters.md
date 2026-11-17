---
id: computing-software.it-support-helpdesk.device-provisioning.joiner-workflow-checklist-and-remote-starters
name: joiner-workflow-checklist-and-remote-starters
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, joiner-checklist, it-orientation, contractor-accounts, remote-device-shipping, scim-provisioning, onboarding]
level: practitioner
status: draft
description: "Run the joiner workflow: lead times and checklist, SCIM provisioning to SaaS, contractor accounts with expiry, shipping devices to remote starters, and day-one IT orientation."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/app-provisioning/user-provisioning"
  - "https://learn.microsoft.com/en-us/entra/identity/users/users-restrict-guest-permissions"
  - "https://learn.microsoft.com/en-us/autopilot/overview"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# joiner-workflow-checklist-and-remote-starters

## Lead times and checklist
HR should trigger the joiner request at least 5-10 working days before the start date.
| Item | Lead time | Owner |
|---|---|---|
| Account (from HR system or request) | 3-5 days | IAM/desk |
| Licences, mailbox, groups by role template | With account | IAM |
| Device ordered or allocated, Autopilot registered | 5-10 days (stock) | Asset team |
| Phone/eSIM, peripherals | 5 days | Desk/telecom |
| Line-of-business app access with approvals | 3-5 days | App owners |
| Building badge (if joint process) | 3 days | Facilities |
Checklist lives in the request (catalog order guide) so each task has an owner and status.

## SCIM provisioning to SaaS
- Entra enterprise app > Provisioning: automatic via SCIM to apps that support it
  (Slack, Zoom, Salesforce, ServiceNow, etc.). Assign users or groups to the app;
  attribute mappings define username, email, department.
- Provisioning cycle every ~40 minutes; "Provision on demand" for one user immediately.
- Errors in provisioning logs (attribute mismatches, duplicate users already in the app).
- Group-based assignment by role means joiners get apps automatically and leavers lose
  them (deprovisioning disables the SaaS account).

## Contractor accounts
- Separate naming or attribute (employeeType = Contractor) and a mandatory **expiry**
  (`accountExpires` in AD; for cloud-only use Entra lifecycle workflows or access
  reviews with auto-removal), sponsor (manager) recorded.
- Least privilege: role-based groups, no standing admin, MFA, usually managed device or
  VDI/Windows 365 for access.
- Extension requires sponsor approval before expiry; expired accounts disabled, not
  deleted, for a retention period.

## Shipping devices to remote starters
- Ship Autopilot-registered devices sealed from the vendor or depot ("white glove"
  pre-provisioned where ESP is heavy) with a one-page quick start: power on, connect to
  Wi-Fi, sign in, what to expect, support number.
- Send the device and the credentials separately: device by courier; temporary access
  pass (TAP) or first-sign-in instructions to the personal email or by phone after ID
  check.
- Track shipment and confirm receipt (serial to user in the asset record); insure and
  require signature for high-value items.

## Day-one IT orientation
- 20-30 minutes (live or recorded): signing in and MFA/passwordless setup, OneDrive and
  where to save, Teams basics, how to get help (portal, phone, chat), security basics
  (phishing reporting button, device lock, travel rules), acceptable use.
- A short welcome article in the KB with the same content.

## Verify
The joiner signs in on day one with the right apps, licence and device; contractor
accounts have expiry and sponsor; shipped devices are recorded as received.
