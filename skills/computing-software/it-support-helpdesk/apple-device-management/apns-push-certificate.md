---
id: computing-software.it-support-helpdesk.apple-device-management.apns-push-certificate
name: apns-push-certificate
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, mdm-protocol, apns-push-certificate, apns, push-certificate]
level: practitioner
status: docs-checked
description: "Network ports and certificate housekeeping for the Apple Push Notification service used by MDM: ports 443, 5223 and 2197, the 17.0.0.0/8 range and annual renewal."
sources:
  - "https://support.apple.com/guide/deployment/dep2de55389a/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apns-push-certificate

Goal: keep MDM push communication working to every managed device.

- MDM services use APNs to keep a persistent connection to Apple devices. An MDM service needs several certificates: an APNs certificate to talk to devices, an SSL certificate for secure communication and a certificate to sign configuration profiles.
- Allow traffic from the devices to the Apple network 17.0.0.0/8, directly or through a proxy. Ports: TCP 443 during device activation (and as fallback if devices cannot reach APNs on 5223), TCP 5223 for device-to-APNs communication, and TCP 443 or 2197 for the MDM service to send notifications to APNs.
- From iOS 13.4, iPadOS 13.4, macOS 10.15.4 or tvOS 13.4, APNs can use a web proxy specified in a proxy auto-config (PAC) file.
- Apple Vision Pro receives push notifications only while worn and unlocked.
- Do not inspect or reroute APNs traffic: the client, APNs and the push provider mark an intercepted conversation as compromised and invalid.
- Note which Managed Apple Account (recommended) or Apple Account created the certificate; you need it to renew, which must be done annually. Certificates are obtained from the Apple Push Certificates Portal.
- Vendor-provided CSRs must be signed with SHA2; the portal will not issue certificates for CSRs signed with SHA1.

Gotcha: renewal needs the same account that created the certificate, so record that account and track the annual expiry; a proxy that inspects APNs traffic breaks the connection.

Verify:
- The expiry date shown in the MDM service is in the team calendar.
- A test device reaches APNs on 5223 (or 443 as fallback) and the MDM service can reach APNs on 443 or 2197.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Configure devices to work with APNs" (ports, 17.0.0.0/8, PAC proxy support, Vision Pro note, renewal tip, SHA2 CSR rule). Corrected: the server ports 2195/2196 in the draft were wrong, Apple lists 443 or 2197. Removed as unconfirmed: the Jamf Pro menu path, the identity.apple.com URL, the "renew, never create new / topic changes / devices must re-enrol" claim, the `com.apple.mgmt.External` topic string, the role-mailbox advice, the 30-day reminder and the unreadable developer.apple.com link.
Method: documentation only; no commands were run.
