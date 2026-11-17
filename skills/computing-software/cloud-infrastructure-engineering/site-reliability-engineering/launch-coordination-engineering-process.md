---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.launch-coordination-engineering-process
name: launch-coordination-engineering-process
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [launch-coordination, lce, launch-review, launch-checklist, sre]
level: practitioner
status: docs-checked
description: "The Launch Coordination Engineer role and launch process as the Google SRE Book describes it: responsibilities, process criteria, checklist curation and low-risk fast paths."
sources: ["https://sre.google/sre-book/reliable-product-launches/", "https://sre.google/sre-book/launch-checklist/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The LCE role and launch review process

Source: SRE Book "Reliable Product Launches at Scale". Google created Launch Coordination Engineering (LCE), a dedicated consulting team within SRE for the technical side of launching a product or feature.

## LCE responsibilities (from the book)
- Auditing products and services for compliance with reliability standards and best practices, providing specific actions.
- Acting as liaison between the teams involved in a launch.
- Driving the technical aspects so tasks keep momentum.
- Acting as gatekeepers and signing off on launches determined "safe".
- Educating developers on best practices and integration with internal services.
Most audits happen before a new product launches. LCEs are SREs held to the same technical requirements, expected to have strong communication and leadership skills, and act as nonpartisan advisors mediating between SRE, developers, product managers and marketing.

## Process criteria
A good launch process is lightweight (easy on developers), robust (catches obvious errors), thorough (addresses important details reproducibly), scalable (many simple launches and fewer complex ones) and adaptable (common and new launch types). The criteria conflict; the book's tactics are simplicity ("get the basics right"), a high-touch approach where experienced engineers customise the process per launch, and fast common paths for classes of launches with a common pattern (for example launching in a new country). The book warns engineers sidestep processes they see as too burdensome.

## Checklist curation
- The checklist gives the LCE a way to assess a launch and gives the team action items and pointers.
- Guidelines: every question's importance must be substantiated, ideally by a previous launch disaster; every instruction must be concrete, practical and reasonable for developers.
- At one point adding a question required vice-president approval to curb growth.
- Continuous small updates, plus a review of the entire checklist once or twice a year to find obsolete items.
- Converging on common infrastructure lets long checklist sections shrink to one line such as "Implement rate limiting using system X".
- For an unusual launch, structure a new checklist around broad themes such as reliability, failure modes and processes, and return to first principles.

## Low-risk fast path
The book's example of a low-risk launch: a feature launch with no new server executables and a traffic increase under 10%, given an almost trivial checklist. By 2008, 30% of reviews were low-risk. A new LCE hire needed about six months of training.

## What LCE did not solve
Scalability changes after success (over two orders of magnitude), growing operational load (SRE's internal goal of keeping operational work below 50%), and infrastructure churn (suggested remedy: a churn reduction policy requiring automated migration for backward-incompatible changes).

## Verify
- [ ] Each launch has a recorded risk-based decision on review depth and a named sign-off owner.
- [ ] The checklist is curated using lessons from past launches.

## Checked
Confirmed against the SRE Book "Reliable Product Launches at Scale" (LCE role, launch process criteria, launch checklist, Development of LCE, Problems LCE Didn't Solve) and the "Launch Coordination Checklist" appendix. Removed: the seven-step intake-to-post-launch process, the one-week post-launch check, the shared launch calendar, the self-service automated gates, and the quarterly checklist revision verify item (the book says once or twice a year).
Method: docs-only read of cited pages, 2026-11-08
