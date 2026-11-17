---
id: computing-software.it-support-helpdesk.intune-mdm.apple-vpp-apps-and-books-distribution
name: apple-vpp-apps-and-books-distribution
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, apps-and-books, apple-vpp, location-token, device-licensing, user-licensing, apple-business-manager, intune]
level: practitioner
status: docs-checked
description: "Distribute iOS and macOS apps bought in Apple Business Manager through Intune: location tokens, device vs user licences, renewal, licence revoke, DDM option and prompts."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/vpp-apps-ios"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apple-vpp-apps-and-books-distribution

Apps purchased in Apple Business Manager (ABM) or Apple School Manager are tied to **location
tokens** (formerly VPP tokens, now "legacy VPP tokens" in Apple's naming). You download the
token from Apple and upload it to Intune, which tracks licence use and tells Apple which
licences to assign to which devices or users; Apple and the device do the installing, not Intune.
Intune supports multiple tokens per tenant (up to 3,000), each valid for one year.

## Token rules
- A location token can serve one MDM at a time. Revoke and remove it from any other MDM
  before using it in Intune; importing it elsewhere afterwards can lose licence assignments
  and user records.
- One Intune tenant per token.
- Intune syncs with Apple once a day by default; you can sync manually. A token marked
  **Duplicate** (same location uploaded twice) stops syncing until the duplicate is removed.

## Create the token
Tenant administration > Connectors and tokens > Apple VPP tokens > Create.
- Basics: token name, Managed Apple Account, token file (ABM > Preferences > Payments and
  Billing > Apps and Books > Content Tokens > Download).
- Settings: *Take control of token from another MDM*, country/region store, type of account
  (Business or Education), **Automatic app updates**, and a **Management type** of MDM
  (default) or DDM. DDM needs iOS/iPadOS 18 or later and supports only Required or Uninstall
  assignments, so do not re-upload a token with existing Available assignments (they are lost).
- Agree to send user and device data to Apple.

## Device vs user licensing
| | Device licensing | User licensing |
|---|---|---|
| Apple Account sign-in | Not needed | Each user needs a unique Apple Account |
| Installs/updates | MDM channel only (Company Portal works) | Needs App Store access; a policy disabling the App Store breaks it |
| User Enrollment | Not supported | Supported with Managed Apple Accounts |
| Books | Not supported | Supported |
| Licences used | One per device | One per user for up to five devices; a person with both a personal and a Managed Apple Account uses two |

New assignments default to **device** licensing. Do not assign both license types to the same
device or user. The Available intent is for user groups only. Device-licensed apps do not show in
Company Portal on User Enrollment devices.

Prompts: user licensing triggers an ABM invitation and an Apple Account prompt; device
licensing on supervised corporate devices installs with no prompts. Avoid user licensing for
kiosk devices.

## Unlimited licenses
Free apps and books can be assigned without a fixed quantity, but not every free app is unlimited
for every location; paid apps still need enough licenses. Acquire the app in ABM for the
location, **Sync** the token, assign.

## Renew
ABM > Preferences > Payments and Billing > Apps and Books > Content Tokens > Download, then in
Intune open the token > Edit on Basics > upload > save. The expiry date may lag; refresh. Also
renew when the Managed Apple ID changes domain, expires or is disabled, which marks the token
invalid.

## Licences and support issues
- Oversubscription is allowed: members beyond the purchased count fail to get a licence. An
  alert appears when used licences are 50% or more of the total.
- Removing an assignment does not reclaim the licence; change the assignment to **Uninstall**,
  which reclaims it and uninstalls the app. Use the **Revoke licenses** action only after
  removing the assignment. On macOS a revoked-licence app stays usable but cannot update, and
  per Apple is removed after 30 days.
- Licences are not reclaimed when a device is removed from Intune. They are reclaimed when the
  user leaves the assigned Entra groups, and revoked when the user is deleted from Entra ID.
- "VPP app is installed but there is a newer version" (0x87D13B9F) is temporary; the install
  command is resent at the next check-in while the assignment remains. Updates can take up to 24
  hours and need the device unlocked. Moving Required to Available stops auto updates until the
  app is reinstalled manually.
- Deleting a token deletes its apps and assignments and revokes licences but does not uninstall
  apps; revoke first, because Intune cannot revoke afterwards.
- Custom roles: Mobile apps permission is enough to view and manage VPP apps; Managed apps
  controls tokens.

## Checked
Date: 2026-11-08. Read in full: Intune "How to Manage iOS and macOS Apps Purchased Through Apple Business Manager with Microsoft Intune" (updated 2026-10-29). The Apple Business Manager and Jamf source pages were landing or empty pages and were dropped. Removed as unconfirmed: Jamf steps, the "Preferences > Payments and Billing" path being the only way to buy, supervised silent-install claims beyond the prompt table, "Pending" and "licence not available" cause tables.
Method: documentation only; no commands were run.
