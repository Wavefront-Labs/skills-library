---
id: computing-software.it-support-helpdesk.intune-mdm.apple-mdm-push-certificate-renewal
name: apple-mdm-push-certificate-renewal
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, apns-certificate, apple-push-notification, mdm-push-certificate, apple-push-certificates-portal, intune, jamf-pro, apple-enrollment]
level: practitioner
status: docs-checked
description: "Renew the Apple MDM push (APNs) certificate for Intune without breaking enrollment: use the same Apple ID, Renew not Create, match the topic GUID, 365-day validity, grace period."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/apple-mdm-push-certificate-get"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apple-mdm-push-certificate-renewal

An Apple MDM push certificate is required to manage iOS/iPadOS and macOS devices in Intune,
whether they enroll through Company Portal or bulk methods (Apple Business, Apple School
Manager, Apple Configurator). It is valid for 365 days and must be renewed annually. After
expiry Intune allows a 30-day grace period to renew. Creating a new certificate instead of
renewing is what forces devices to re-enroll (the Intune troubleshooting page for
`APNSCertificateNotValid` says to renew, not replace).

## Renew
1. Intune admin center > Devices > Device onboarding > Enrollment > **Apple** tab >
   **Apple MDM Push Certificate**. Note the Apple ID shown.
2. **Download your CSR**.
3. **Create your MDM push Certificate** opens the Apple Push Certificates Portal. Sign in with
   the **same Apple ID** that created the certificate.
4. Find the certificate and choose **Renew** (not Create a Certificate). Choose the new CSR
   and enter a unique note so you can identify it later. Upload, then Download the `.pem`.
5. Back in Intune upload the `.pem`. Renewal is complete when the status shows active in both
   the admin center and the Apple portal.

To tell which certificate is which: each has a unique UID, and the portal's subject ID shows
its GUID. On an enrolled iPhone, Settings > General > Device Management > Management Profile
> More Details > Management Profile, the **Topic** value holds the GUID to match.

## Prevent the outage
- The certificate is tied to the Apple ID used to create it. Use a company email address
  whose mailbox is monitored by more than one person (for example a distribution list), not a
  personal Apple ID.
- Entering the Apple ID in Intune (step 4 of creation) is what lets Intune remind you to renew.
- If you change the Apple ID later, sign in to the portal with the new ID, download the
  certificate again and upload it in Intune with the new Apple ID.
- If you will federate Entra accounts with Apple Managed Apple IDs, ask Apple to migrate the
  existing push certificate to the new Managed Apple ID.

## Verify
Intune shows the new expiry (365 days ahead) and an active status in both consoles.

## Checked
Date: 2026-11-08. Read in full: Intune "Get an Apple MDM push certificate" (updated 2026-04-09), plus the iOS enrollment errors page for the renew-not-replace statement. The Apple deployment guide and Apple Push Certificates portal sources were dropped (the guide landed on a contents page; the portal needs sign-in). Removed as unconfirmed: all Jamf instructions, 30 and 7 day reminder advice, network ports and hostnames for APNs, the renewal-after-30-days behaviour, "different Apple ID creates a new topic", and the .pem renaming note.
Method: documentation only; no commands were run.
