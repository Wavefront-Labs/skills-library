---
id: computing-software.digital-privacy-hygiene.privacy-configuration.edge-privacy-settings
name: edge-privacy-settings
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, edge-privacy, windows-privacy, browser-hardening]
level: practitioner
status: docs-checked
description: "Tighten Microsoft Edge: tracking prevention levels and exceptions, plus the policy names behind diagnostics, personalisation, shopping, suggestions, secure DNS, SmartScreen."
sources:
  - "https://support.microsoft.com/microsoft-edge/learn-about-tracking-prevention-in-microsoft-edge-5ac125e8-9b90-8d59-fa2c-7f2e9a44d869"
  - "https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Edge privacy settings

**Goal:** if you use Edge (default on Windows, or a work requirement), reduce tracking and data sent to Microsoft.

## Tracking prevention (documented UI path)
Settings and more > Settings > **Privacy, search, and services** > **Tracking prevention**, make sure it is On, then
pick a level (Microsoft's descriptions):
- **Basic:** blocks potentially harmful trackers; allows most others, including those that personalise content and ads.
- **Balanced (Recommended):** blocks harmful trackers and trackers from sites you have not visited; content and ads
  likely less personalised.
- **Strict:** blocks harmful trackers and most trackers across sites; minimal personalisation. It can break sites, for
  example a video may not play or sign-in may fail.

Exceptions: Tracking prevention > **Exceptions** > Add a site (full URL), or on the site choose View site
information (left of the address bar) and turn Tracking prevention for this site off. Exceptions allow all trackers
on that site, including harmful ones. View site information > **Trackers** shows what the site uses and how many were
blocked.

## Other controls Microsoft documents as policies
The Edge policy list names a control for each of these. Policy names are the stable handle: on a managed PC they are
set by an administrator, and on your own PC look for the matching switch in Privacy, search, and services (labels not
checked).
| Aim | Policy name |
|---|---|
| Limit diagnostic data | `DiagnosticData` ("Send required and optional diagnostic data about browser usage") |
| Stop sending browsing data for personalisation | `PersonalizationReportingEnabled` |
| Shopping feature off | `EdgeShoppingAssistantEnabled` ("Shopping in Microsoft Edge") |
| No web service for navigation errors | `ResolveNavigationErrorsUseWebService` |
| No "similar pages" suggestion | `AlternateErrorPagesEnabled` |
| Search suggestions | `SearchSuggestEnabled` |
| Secure DNS | `DnsOverHttpsMode`, `DnsOverHttpsTemplates` (resolver URI template) |
| Safe-browsing style protection | `SmartScreenEnabled` (Microsoft Defender SmartScreen), `TyposquattingCheckerEnabled` (Website Typo Protection) |
| Tracking prevention level | `TrackingPrevention` |

## Gotchas
- Work-managed Edge settings may be locked by an administrator through these policies.
- Strict mode can block embedded content or logins; use an exception for a trusted site.

## Checked
Checked 2026-11-08 against the full text of Microsoft's "Learn about tracking prevention in Microsoft Edge" and the
Edge policy list (names and one-line titles only). Removed what neither states: exact setting labels and
recommended values for InPrivate strict mode, Do Not Track, optional diagnostic data, the sidebar and Copilot page-access
switch, and the claim that Edge sync is not end-to-end encrypted for all data types, and the edge://policy page.
Method: documentation only; no commands were run.
