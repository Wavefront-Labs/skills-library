---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.gpl-enforcement-and-remediation
name: gpl-enforcement-and-remediation
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [gpl-enforcement-and-remediation, gpl-obligations-and-faq, gpl-violation, enforcement, cure, reinstatement, gpl-3-section-8, cease-and-desist, itam-licence-compliance]
level: sme
status: docs-checked
description: "Respond to a GPL violation claim using GPL-3.0 section 8 (termination, reinstatement, cure) and the GNU GPL FAQ on who enforces; legal review required."
sources:
  - https://spdx.org/licenses/GPL-3.0-only.html
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPL violation response and remediation

Goal: cure quickly and reduce legal risk. This skill reports what the licence text and FAQ say; it is not legal advice. Route every claim to legal counsel.

What the texts say:
- Section 8 of GPL-3.0: you may not propagate or modify a covered work except as the licence expressly provides; any other attempt is void and automatically terminates your rights under the licence, including patent licences granted under section 11.
- Reinstatement (section 8): if you cease all violation, your licence from a particular copyright holder is reinstated (a) provisionally, unless and until that holder explicitly and finally terminates it, and (b) permanently if the holder fails to notify you of the violation by some reasonable means before 60 days after the cessation.
- Also permanently reinstated if the holder notifies you, it is the first notice of violation you have received from that holder (for any work), and you cure the violation before 30 days after receiving the notice.
- Termination of your rights does not terminate the licences of parties who received copies or rights from you. While rights are terminated and not permanently reinstated, you do not qualify to receive new licences for the same material under section 10.
- The FAQ: to "cure" a violation of GPLv3 means to adjust your practices to comply with the licence. The GPL is a copyright licence enforced by the copyright holders, so report or answer to the holder of the program concerned. The FAQ says the termination conditions of GPLv3 are considerably more permissive than GPLv2's, so check which version the code is under before relying on the above.

Method:
1. Preserve evidence, route to legal, and stop distributing affected builds while the facts are established (section 8 ties your rights to compliance).
2. Identify components, versions and licence versions shipped; check every distribution channel (firmware, apps, containers).
3. Cure: comply with the licence for each affected component (for example provide the Corresponding Source and licence notices, or remove or replace the component) as counsel advises.
4. Contact the claimant, show the cure, and record the dates; the 30 and 60 day periods in section 8 run from notice and cessation respectively.
5. Prevent recurrence: a licence and SBOM check in the build pipeline and a release gate with legal approval (your own process, not a licence requirement).

Verify: a release checklist exists in the pipeline and the cure dates are recorded.

## Checked

2026-11-08. Confirmed against the GPL-3.0 text on spdx.org (section 8 termination and both reinstatement routes, effect on downstream licensees, section 10 consequence) and the GNU GPL FAQ (definition of cure, who enforces, GPLv3 termination more permissive than GPLv2). Removed: "past violations remain claims for damages", and "silence escalates", as no fetched page supports them; the reinstatement point that needed confirming is now stated from the text. Step 5 is marked as a process suggestion.
Method: documentation only; no commands were run.
