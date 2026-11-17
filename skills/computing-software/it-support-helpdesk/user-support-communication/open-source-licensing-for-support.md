---
id: computing-software.it-support-helpdesk.user-support-communication.open-source-licensing-for-support
name: open-source-licensing-for-support
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, open-source-licensing, gpl, copyleft, software-approval, comptia-a-plus]
level: practitioner
status: draft
description: "Handle open-source software in support: identify the licence, tell permissive from copyleft, what internal use vs redistribution means, approved lists and SBOM records."
sources:
  - https://opensource.org/licenses
  - https://spdx.org/licenses/
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Open-source licensing for support staff

Open source is free to obtain, but it still carries a licence with conditions. Support staff decide whether a requested tool can be installed and must spot when a request needs legal or security review.

## Identify the licence
- Check the project's `LICENSE`/`COPYING` file, repository sidebar, package metadata, or SPDX identifier (e.g. `MIT`, `Apache-2.0`, `GPL-3.0-only`).
- No licence file = all rights reserved by default; not free to use commercially. Escalate.

## Families
| Family | Examples | Key conditions |
|---|---|---|
| Permissive | MIT, BSD-2/3-Clause, Apache-2.0 | Keep copyright and licence notices; Apache adds patent grant and NOTICE file |
| Weak copyleft | LGPL, MPL-2.0, EPL | Changes to the library itself must be shared if distributed |
| Strong copyleft | GPL-2.0/3.0 | Distributing the software or derivatives requires source under GPL |
| Network copyleft | AGPL-3.0 | Offering modified software over a network triggers source sharing |
| "Source available" | BSL, SSPL, Elastic, Commons Clause | Not OSI open source; commercial use restrictions; check terms |

## Practical rules
- **Internal use** of unmodified GPL/AGPL tools (e.g. installing GIMP, Inkscape) generally creates no obligation; obligations attach to **distribution** (or network service for AGPL).
- Embedding open-source code in products the company ships, or modifying AGPL services, goes to the developers' open-source policy/legal.
- Dual-licensed or "free for personal use" tools may need a commercial licence at work.
- Use the organisation's **approved software list**; requests for new tools go through security review (maintenance status, CVEs, publisher, download source).
- Download from the official project or a trusted package manager (winget, Chocolatey internal feed), not mirror sites bundling adware.

## Records
Record approved tools with version, licence (SPDX ID) and source in the software catalogue/CMDB; development teams keep SBOMs (SPDX/CycloneDX).

## Verify
The ticket notes the licence, approval reference and download source before installation.
