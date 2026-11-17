---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.agpl-section-13
name: agpl-section-13
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [agpl-section-13, agpl-and-network-use, agpl-3-0, section-13, remote-network-interaction, saas-copyleft, modified-version, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Determine when running modified AGPL software as a service requires offering source to remote users."
sources:
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AGPL section 13 remote network interaction

Goal: know when AGPL duties start.

Rule: if you run a modified version of AGPL software and users interact with it remotely through a network, you must offer all of those users an opportunity to receive the source of your modified version (the GNU GPL FAQ gives a company running a modified AGPL program on a web site as the example).
Running a modified GPL (not AGPL) program as a service does not trigger this: the GPL lets you modify and use a program without ever distributing it.

What counts as remote interaction (GPL FAQ):
- A program expressly designed to accept user requests and send responses over a network (web and mail servers, interactive web applications, online game servers) meets the test.
- A program that merely happens to run over a network (for example via SSH or a remote X session) does not.
- The test is whether a person can reasonably be expected to interact with it remotely, whether you call it a client or a server.
- For a proxy, deliver the offer through the proxy's normal message channel (a web proxy can use a landing page). You need not repeat the offer to a user already shown it for the current version.

What the offer must include: the Corresponding Source defined in section 1 of the licence. That covers libraries your modified version depends on (for example Expat or GPLv3 code), with your modifications to them, unless they are System Libraries.

Method:
- Inventory AGPL components in services (databases, CMS, analytics).
- Decide: use unmodified, publish the modifications, or buy a commercial licence.
- Put a source offer where users reach the service and keep it matching the deployed version.

Gotchas:
- Many enterprises ban AGPL by policy; check yours.
- GPLv3 and AGPLv3 modules may be linked together in either direction (GPL FAQ); the Corresponding Source offered still includes the code combined with the Program.

Verify: deployed version and published source match.

## Checked

2026-11-08. Confirmed against the GNU GPL FAQ (gpl-faq.html): the AGPL requirement to offer source to all users interacting remotely, the web-site example, the interacting-remotely criteria, the SSH/remote X exclusion, the proxy answer, the Corresponding Source answer, GPL/AGPL linking, and that modified GPL use without distribution need not release source. Removed: the claim that unmodified AGPL software never triggers section 13 duties (the FAQ only addresses modified versions) and the claim that linking AGPL libraries makes the whole service a combined work (not stated on the page). The AGPL licence text itself was not readable in this session, so section numbers beyond those the FAQ names were not checked.
Method: documentation only; no commands were run.
