---
id: computing-software.it-support-helpdesk.apple-device-management.sso-extension-kerberos
name: sso-extension-kerberos
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, platform-sso, sso-extension-kerberos, sso-extension, kerberos]
level: practitioner
status: docs-checked
description: "Deploy the Kerberos variant of the Extensible SSO payload so Apple devices obtain Active Directory tickets for on-premises resources."
sources:
  - "https://support.apple.com/guide/deployment/kerberos-sso-extension-depe6a1cda64/web"
  - "https://support.apple.com/guide/deployment/platform-sso-for-mac-dep7bbb05313/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.extensiblesso%28kerberos%29.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sso-extension-kerberos

Goal: silent sign-in to on-premises Active Directory resources.
- Payload `com.apple.extensiblesso`, Kerberos variant (macOS 10.15 or later, iOS 13 or later, visionOS 1.1 or later). Required: `ExtensionIdentifier` = `com.apple.AppSSOKerberos.KerberosExtension`, `TeamIdentifier` = `apple`, `Type` = `Credential`, and `Realm` (written with proper capitalisation).
- `Hosts`: array of hostnames and domains the extension handles; case-insensitive, a leading "." matches any subdomain, and each value must be unique across all Extensible SSO payloads on the device.
- `ExtensionData` keys include `principalName`, `siteCode`, `useSiteAutoDiscovery`, `certificateUUID`, `credentialBundleIdACL`, `allowPasswordChange`, `preferredKDCs`, `usePlatformSSOTGT` and `syncLocalPassword`. With Platform SSO, set `syncLocalPassword` to false in the Kerberos configuration.
- Requirements from the page: an Active Directory domain on Windows Server 2008 or later (not Microsoft Entra ID alone), and network reach to the domain controllers by Wi-Fi, Ethernet or VPN. On iOS the extension activates on an HTTP 401 Negotiate response; on macOS it acquires the ticket-granting ticket proactively, usually valid for 10 hours.
- Tools named on the page: `app-sso` reads the extension state and can request common actions such as sign in; `klist`, `kinit` and `kdestroy` manage tickets.
Practice: test with a user off the corporate network, since tickets need a reachable domain controller (or VPN).
Gotcha: a `Hosts` value already used by another Extensible SSO payload conflicts; keep one owner per host.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Deployment "Kerberos Single Sign-on extension" and the Kerberos Extensible SSO payload YAML from apple/device-management; Platform SSO for Mac (the Kerberos combination paragraph only is used; the rest was skimmed).
- Removed as unconfirmed: the `CredentialUseMode` key (not in the payload definition), "uppercase realm" (the page says proper capitalisation), DNS SRV record advice, the `app-sso -l` flag, pairing with Jamf Connect, the certificate-payload-for-trust advice, and the Verify steps.
- The original second source (learn.microsoft.com macOS Platform SSO page) resolves but has no `app-sso` or Kerberos ticket content, so it was dropped; the first source ID was not a real page.
