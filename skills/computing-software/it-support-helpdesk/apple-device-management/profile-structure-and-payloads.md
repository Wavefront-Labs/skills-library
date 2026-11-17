---
id: computing-software.it-support-helpdesk.apple-device-management.profile-structure-and-payloads
name: profile-structure-and-payloads
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, config-profiles, profile-structure-and-payloads, payloads, plist, mobileconfig]
level: practitioner
status: draft
description: "Read and build the plist structure of a configuration profile, including PayloadType, PayloadIdentifier and UUID keys, so custom payloads install cleanly."
sources:
  - "https://support.apple.com/guide/deployment/configuration-profiles-and-payloads-dep9c8f4f2a0/web"
  - "https://developer.apple.com/documentation/devicemanagement/profile-specific_payload_keys"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# profile-structure-and-payloads

Goal: author or inspect a `.mobileconfig` correctly.
- Top-level keys: PayloadContent (array), PayloadType `Configuration`, PayloadIdentifier, PayloadUUID, PayloadVersion 1, PayloadDisplayName, PayloadScope (System or User), PayloadOrganization.
- Each payload repeats Type (e.g. `com.apple.wifi.managed`), Identifier, UUID and Version plus its own keys.
- Build with iMazing Profile Editor, ProfileCreator or Apple Configurator; Jamf wraps payloads in Configuration Profiles.
- Validate with `plutil -lint file.mobileconfig`.
- Custom settings: upload a preference domain plus plist through a Custom Settings payload.
Practice: Keep one payload domain per profile where practical so a faulty Wi-Fi entry does not block restrictions, and store source `.mobileconfig` files in git with a review step before upload.
Gotcha: re-using a PayloadIdentifier with new content but the same UUID can stop updates applying; change the UUID when content changes outside an MDM.
Verify:
- `plutil -lint` returns OK.
- `profiles show` lists the identifier after install.
