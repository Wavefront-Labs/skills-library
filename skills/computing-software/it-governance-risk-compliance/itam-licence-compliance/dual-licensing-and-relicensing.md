---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.dual-licensing-and-relicensing
name: dual-licensing-and-relicensing
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [dual-licensing-and-relicensing, contribution-and-relicensing, dual-licensing, relicensing, copyright-assignment, contributor-consent, license-change, itam-licence-compliance]
level: sme
status: docs-checked
description: "Dual-license or relicense a project: who may do it according to the GNU GPL FAQ, MPL-2.0 and the Apache GPL-compatibility page, and what to trace first."
sources:
  - https://www.gnu.org/licenses/gpl-faq.html
  - https://www.apache.org/licenses/GPL-compatibility.html
  - https://www.mozilla.org/en-US/MPL/2.0/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual licensing and relicensing a project

Goal: understand who can offer extra licence terms and what to establish first. This skill reports published statements; it is not legal advice, so have counsel confirm before a licence change.

Method:
- Who can license: the GNU GPL FAQ says the GPL does not give users permission to attach other licences to a program, but the copyright holder can release it under several different licences in parallel, one of which may be the GPL. A copyright holder can release it under various different non-exclusive licences at various times. The licence in your legitimately obtained copy, if put there by the copyright holder, is the one that applies to that copy.
- Only copyright holders can add exceptions: per the FAQ, you cannot add an exception to someone else's GPL-covered code; only its copyright holders can.
- So before offering a second licence, list every copyright holder of the code you want to cover. Use the project's version history and contribution records to do this, and check any contributor agreements (assignment, disclaimer or licence grant). The FAQ describes the FSF approach of asking contributors to assign copyright or disclaim it, to keep the copyright status simple enough to enforce.
- The FAQ also says the developer of a GPL-covered program is not bound by the GPL, because it is a licence from the developer to others (a developer's own actions are strictly not a GPL violation).
- Third-party components: a second licence only covers what you own. For code under other licences, read each licence and, for MPL-2.0, its section 3.3 on distributing a Larger Work; MPL-2.0 defines a Secondary License as the GNU GPL 2.0, LGPL 2.1, AGPL 3.0 or later versions of those.
- Some projects decline dual licensing as policy: the Apache Software Foundation says it will not dual-license its software.
- Announce changes against a version boundary and keep the previous release's licence file with that release; the FAQ states the licence that came with your copy governs that copy.

Gotchas:
- Contributors without a grant or assignment that covers the new terms are a gap; whether their consent or removal of their code is required is a legal judgment, so get advice.
- Mixed copyright ownership blocks single-owner decisions.

Verify: a contributor audit lists each copyright holder with the grant, assignment or consent that covers the new licence, or marks their code for removal.

## Checked

2026-11-08. Confirmed against the GNU GPL FAQ (parallel and non-exclusive licensing, licence in the copy applies, only copyright holders add exceptions, developer not bound by the GPL, FSF assignment/disclaimer practice), the Apache GPL-compatibility page (ASF will not dual-license) and the MPL-2.0 text (Secondary License definition, section 3.3 exists). Removed: git commands (not a documentation claim), the assertion that every contributor's consent is required without a CLA, the clean-room claim and the fork claim, because no fetched page states them. Section 3.3 body text was not readable from the fetched pages, so it is only cited by name.
Method: documentation only; no commands were run.
