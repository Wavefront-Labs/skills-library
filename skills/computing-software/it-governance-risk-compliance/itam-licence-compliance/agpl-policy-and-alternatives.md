---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.agpl-policy-and-alternatives
name: agpl-policy-and-alternatives
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [agpl-policy-and-alternatives, agpl-and-network-use, agpl-policy, agpl-section-13, remote-network-interaction, commercial-licence, dual-licence, alternatives, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Write an AGPL policy from what AGPL-3.0 section 13 and the GNU GPL FAQ say, and evaluate commercial or alternative licences for AGPL dependencies."
sources:
  - https://spdx.org/licenses/AGPL-3.0-only.html
  - https://opensource.org/license/agpl-3.0
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AGPL policy, commercial licences and alternatives

Goal: decide quickly when AGPL appears. This skill reports what the licence text and the FSF FAQ say; it is not legal advice, so route edge cases to counsel.

Method:
- What AGPL-3.0 adds: section 13 ("Remote Network Interaction; Use with the GNU General Public License") applies if you modify the Program. Your modified version must prominently offer all users interacting with it remotely through a computer network an opportunity to receive the Corresponding Source of your version, from a network server at no charge.
- The FAQ says the test is whether the program is expressly designed to accept user requests and send responses over a network (web and mail servers, interactive web applications, online game servers). A program that merely happens to be run over SSH or a remote X session is not covered. It also says it does not matter whether you call the program a client or a server.
- Running an unmodified AGPL program: section 13 is triggered by modification. Whether your usage is "modified" is a fact question to settle with counsel, not by this skill.
- Combining with GPL-3.0: section 13 of AGPL-3.0 gives permission to link or combine any covered work with a work licensed under version 3 of the GPL into a single combined work; each part stays under its own licence. The FAQ confirms the two licences explicitly permit linking in both directions.
- Policy tiers are your own risk choice, not something the licence defines. A workable set: allowed as separate tools you do not modify; needs review if modified, embedded or exposed to users over a network; banned in products you distribute unless legal approves.
- Commercial licence or alternative: the FAQ says a copyright holder can release a program under several licences in parallel, and the licence in your legitimately obtained copy is the one that applies to it. So a commercial licence is only available if the copyright holder(s) offer one; ask the vendor. Compare its cost (see the vendor's own pricing; none is recorded here) against the engineering cost of replacing the dependency.
- Record the decision with the dependency name, version and licence variant (for example AGPL-3.0-only versus AGPL-3.0-or-later, per its SPDX identifier), and review it at major upgrades.

Gotchas:
- Licences are per work. Check the licence of each package (server, client library, plugin) separately; do not assume they share one.
- Only the copyright holders can grant different terms or add exceptions; a fork cannot offer a commercial licence for code it does not own.

Verify: the approval record names the licence variant, the section 13 analysis (modified or not, network-facing or not) and the rationale.

## Checked

2026-11-08. Confirmed against the AGPL-3.0 text on spdx.org (section 13 wording, GPL-3.0 combination permission), the AGPL-3.0 page on opensource.org, and the GNU GPL FAQ (network-interaction test, SSH/remote X example, client or server, AGPL-GPL linking, parallel licensing, only copyright holders can add exceptions). Removed: the claim about named AGPL vendors with dual licensing, the CLA claim, and the claim that client libraries are usually permissive, because no fetched page supports them. The tier policy is presented as a suggestion, not a licence rule. The earlier ISO, CycloneDX, NTIA, OpenChain and REUSE sources supported none of the remaining claims and were dropped.
Method: documentation only; no commands were run.
