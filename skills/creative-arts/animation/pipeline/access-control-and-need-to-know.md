---
id: creative-arts.animation.pipeline.access-control-and-need-to-know
name: access-control-and-need-to-know
category: creative-arts
field: animation
product: pipeline
tags: [access-control, need-to-know, least-privilege, content-security, tpn, mpa, permissions]
level: practitioner
status: draft
description: "Apply access control to unreleased animation content: need-to-know, role-based permissions, MFA, joiner-mover-leaver process, access reviews, logging and vendors."
sources:
  - https://www.ttpn.org/
  - https://www.motionpictures.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Access control and need-to-know

Studios and distributors require partners to protect unreleased content. The Motion Picture Association's content security best practices and the Trusted Partner Network (TPN) assessments describe the expected controls; obtain the current versions from them, since requirements are updated. This skill covers practical access control.

## Principles
- **Need-to-know**: a person gets access only to the shows, episodes and areas they need to do their work.
- **Least privilege**: grant the minimum permission (read, write, delete) required.
- **Individual accounts**: no shared logins, so actions are attributable.

## Implementation
1. **Roles**: define roles (artist, lead, production, IT admin, vendor) and map roles to permissions on storage, tracker, review tools and render farm.
2. **Project-based groups**: access follows project membership; remove people from the group when they leave the show.
3. **Authentication**: multi-factor authentication for remote and admin access, VPN or zero-trust access for remote artists.
4. **Joiners, movers, leavers**: onboarding grants a role bundle; role changes trigger a review; leaving triggers same-day removal across all systems, including vendor and tracker accounts.
5. **Access reviews**: periodic reviews (many programmes expect at least quarterly or per-project) where leads confirm each person's access.
6. **Logging**: log logins, access to sensitive folders and large downloads, and review the logs; protect them from tampering.
7. **Separate environments**: restrict external-facing systems and keep the production network segmented from general office or guest networks.
8. **Physical**: controlled areas, visitor logs and clean-desk rules for secure rooms.

## Vendors and freelancers
- NDAs and security requirements flow down to vendors; check if their facility is TPN-assessed where a distributor requires it.
- Give vendors access only to their shots, expiring on the end date (`secure-file-transfer-and-screeners.md`).

## Verify
- [ ] Every account is individual, with MFA where required.
- [ ] Leaver removal tested end to end.
- [ ] Last access review date is recorded.
