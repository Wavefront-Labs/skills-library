---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.microsoft-remote-desktop-and-other-rights
name: microsoft-remote-desktop-and-other-rights
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [microsoft-remote-desktop-and-other-rights, microsoft-licensing, rds cal, visual studio subscription, dev test, extended security updates, msdn, windows vda, itam-licence-compliance]
level: advanced
status: draft
description: "Handle RDS CALs, Visual Studio subscriptions, dev/test and extended security update rights correctly."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Microsoft RDS CALs, Visual Studio and special rights

Goal: cover edge products that audits often catch.

- RDS CAL: needed in addition to Windows Server CAL for each user or device using remote desktop services.
- Visual Studio subscriptions: licence each person who uses software (not each machine); subscription software for development and test only, not production.
- VDI access to Windows client: Windows VDA or Windows Enterprise rights through SA/subscription.
- Extended Security Updates: purchased per device for end-of-support products; confirm availability and enrolment via Azure Arc.
- Dev/Test pricing in Azure requires VS subscribers.

Method: add these items into your ELP template and discovery rules (RDS role detection).

Gotchas:
- Production use of MSDN software is a classic finding.
- Terms change annually; check the Product Terms.

Verify: RDS hosts list matches CAL purchases.
