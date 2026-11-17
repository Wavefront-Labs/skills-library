---
id: computing-software.it-support-helpdesk.apple-device-management.admin-demotion-and-privilege
name: admin-demotion-and-privilege
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, local-admin, admin-demotion-and-privilege, admin-rights, privileges, elevation]
level: practitioner
status: draft
description: "Remove standard-user admin rights and offer time-limited elevation with a privileges tool or Jamf Connect."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Local_Accounts.html"
  - "https://support.apple.com/guide/deployment/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# admin-demotion-and-privilege

Goal: least privilege without breaking support.
- Audit admins: `dscl . read /Groups/admin GroupMembership`.
- Demote: `dseditgroup -o edit -d username -t user admin`.
- Offer elevation via SAP Privileges app (time-limited) or Jamf Connect Privilege Elevation (confirm product).
- Log elevation to the MDM.
- Document exceptions and review monthly.
Practice: Communicate the change ahead of time, give a quick way to request elevation, and watch the ticket queue for installers that need a permanent solution. Keep one audited break-glass admin per Mac for emergencies.
Gotcha: some installers still prompt for an admin password; deploy them through MDM which runs as root.
Verify:
- Test user cannot install system software.
- Elevation expires after the set time.
