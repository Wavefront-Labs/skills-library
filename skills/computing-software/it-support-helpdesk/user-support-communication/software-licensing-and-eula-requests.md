---
id: computing-software.it-support-helpdesk.user-support-communication.software-licensing-and-eula-requests
name: software-licensing-and-eula-requests
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, privacy, eula, software-licensing, open-source-licenses, personal-vs-corporate-use, freeware-commercial-use, drm, licence-compliance, comptia-a-plus]
level: practitioner
status: draft
description: "Handle software requests with licensing in mind: EULA personal vs commercial use, licence models, open-source licences, and refusing unlicensed installs."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://opensource.org/licenses"
  - "https://www.bsa.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# software-licensing-and-eula-requests

Goal: everything installed on company devices is licensed for how the
company uses it (A+ 220-1202 4.6 licensing/DRM/EULA).

## License models you'll meet
| Model | Watch for |
|---|---|
| Per user (named) | reassign on leavers; one user, multiple devices |
| Per device | counts installs; reimaged devices may double-count |
| Concurrent/floating | licence server; "no licences available" tickets |
| Subscription (SaaS) | lapses silently; tied to account |
| Perpetual + maintenance | version rights end when maintenance ends |
| Site/enterprise agreement | true-up audits annually |
| Freeware/free for personal use | **often not free for commercial use** (e.g. some archivers, media tools, "community" editions with company-size limits) |
| Open source | MIT/BSD/Apache permissive; GPL obligations matter if redistributing/modifying — usually fine for internal use |

## Handling a request
1. Is there an approved tool already doing the job? Offer it.
2. Read the EULA/licence page for **commercial use** and organisation size
   limits (e.g. free tiers capped at small businesses).
3. Licence available in the pool? Assign it via the licence management
   process (SAM tool, group-based assignment).
4. Not licensed → route to procurement with cost and justification; don't
   install trial versions to "tide them over" unless trials are permitted.

## Refusals
"Downloaded a cracked/keygen version" or personal licence keys on company
devices: remove, explain (legal and malware risk), log for SAM. Users
bringing their own personal licence: generally not allowed — licences are
usually non-transferable to employers.

## DRM
DRM-protected content (e-books, streaming) on corporate devices: follow
policy; circumventing DRM is unlawful in many jurisdictions — don't help.

## Gotchas
- Vendor audits (Microsoft, Oracle, Adobe, Autodesk) use install data; the
  desk's installs create the exposure.
- Java SE and some database editions changed commercial licensing — check
  current terms before deploying.

## Verify
Installs reconcile with entitlements in the SAM tool; no "free for personal
use" tools in the software inventory.
