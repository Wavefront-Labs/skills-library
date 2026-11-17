---
id: computing-software.systems-network-administration.backup-and-recovery.iscp-recovery-roles-and-teams
name: iscp-recovery-roles-and-teams
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [iscp-recovery-roles, recovery-team, contingency-plan, iscp, dr-runbook]
level: practitioner
status: docs-checked
description: "Define ISCP recovery teams and roles per NIST SP 800-34r1 section 3.4.6: management team, team leaders and alternates, staffing, and authority to activate."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ISCP roles and recovery teams

After choosing backup and recovery strategies, the ISCP Coordinator must designate teams to carry them out (SP 800-34r1 section 3.4.6). Each team is trained and ready for plan activation, and assigned to respond to the event, recover capabilities and return the system to normal operations.

## Team members must understand
The team's recovery goal, the individual procedures it will execute, and how interdependencies between recovery teams affect overall strategy.

## Teams
Types depend on the affected system and can be tailored to FIPS 199 impact levels. Size, titles and hierarchy depend on the organisation. Besides a single authoritative role for overall decision-making, including plan activation, NIST lists some or all of:
- Management team (including the ISCP Coordinator)
- Outage assessment team
- Operating system administration team
- Server recovery team (for example client server, web server)
- LAN/WAN recovery team
- Database recovery team
- Network operations recovery team
- Application recovery team(s)
- Telecommunications team
- Test team
- Transportation and relocation team
- Media relations team
- Legal affairs team
- Physical/personnel security team
- Procurement team (equipment and supplies)

## Staffing
- Choose by skills and knowledge; ideally staff with people who do the same or similar work normally (server recovery team includes the server administrators).
- Teams should be big enough to stay viable if some members are unavailable, or name alternate members.
- Members should know other teams' goals and procedures to coordinate.
- If a disruption leaves staff unavailable, personnel from another geographic area or contractors or vendors may be needed; coordinate and train them as an alternate team.

## Team leaders
Each team has a leader who directs team operations, represents the team to management, liaises with other team leaders, disseminates information and approves team decisions. Name a designated alternate leader.

## Management team
Provides overall guidance after a major disruption: activates the plan, supervises contingency operations, facilitates communication among teams and supervises ISCP tests and exercises. A senior management official such as the CIO has ultimate authority to activate the plan and decide spending levels, acceptable risk and interagency coordination, and typically leads the management team.

## Verify
Every team has a leader, an alternate leader, named members, and written goals and procedures; the activation authority is named.

## Checked

2026-11-09. Read NIST SP 800-34 Rev. 1 section 3.4.6. Removed: the roles table (plan owner, ISCP Director, ISSO, communications lead; not defined that way in this section), RACI mapping, break-glass and offline-contact rules and the quarterly contact verification (not stated). The draft cited a "Section 4" for this content; it is section 3.4.6.

Method: documentation only; no commands were run.
