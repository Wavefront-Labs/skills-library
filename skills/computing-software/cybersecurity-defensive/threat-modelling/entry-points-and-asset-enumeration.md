---
id: computing-software.cybersecurity-defensive.threat-modelling.entry-points-and-asset-enumeration
name: entry-points-and-asset-enumeration
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [entry-points, asset-enumeration, attack-surface, threat-modelling, exit-points, trust-levels]
level: practitioner
status: docs-checked
description: "Enumerate a system's entry points, exit points, assets and trust levels using OWASP's documented fields, and map and bucket the attack surface."
sources: ["https://owasp.org/www-community/Threat_Modeling_Process", "https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entry points and asset enumeration

OWASP's threat modelling process decomposes an application into external dependencies, entry
points, exit points, assets and trust levels before identifying threats.

## Documenting each item (OWASP Threat Modeling Process)
- **Entry points:** interfaces through which an attacker can interact with the application or
  supply it with data; they can be layered (each web page may hold several). Fields: ID
  (cross-referenced from threats; use major.minor for layered points), Name, Description,
  Trust Levels (the access level required, cross-referenced to the trust level table).
- **Exit points:** where data leaves the system (dynamic output, methods). Entry and exit
  points together define a trust boundary. Exit points matter for attacks such as
  cross-site scripting and information disclosure, and for components holding confidential
  data. Threats at an exit point often relate to the matching entry point: login error messages
  can enable account harvesting ("username not found") or reveal SQL errors.
- **Assets:** things attackers are interested in, physical (a client list with personal
  information) or abstract (an organisation's reputation, though OWASP says it is unclear how
  that helps threat modelling). Fields: ID, Name, Description (what it is and why it needs
  protecting), Trust Levels.
- **Trust levels:** the access rights the application grants external entities, each with an
  ID, Name and Description, cross-referenced with entry points and assets to define the
  privileges required at each entry point and for each asset.
- **External dependencies:** items outside the application code that may pose a threat, often
  still within the organisation's control but not the development team's, for example the
  assumed production environment (a hardened server behind a firewall). Fields: ID and
  Description.

## Mapping the attack surface (OWASP Attack Surface Analysis cheat sheet)
- The attack surface is all paths for data and commands into and out of the application, the
  code protecting those paths, the valuable data (secrets, keys, IP, business data, PII) and
  the code protecting that data. Overlay user roles and privilege levels, and focus on the
  extremes: anonymous users and highly privileged admins.
- Start with design documents and source code, from the attacker's view, listing entry and
  exit points such as UI forms and fields, HTTP headers and cookies, APIs, files, databases,
  other local storage, messages, and runtime arguments.
- Because the count can reach thousands, group points into types (login/authentication, admin
  interfaces, search, CRUD forms, business workflows, transactional APIs, operational command
  and monitoring interfaces, interfaces with other systems), count each type, pick sample cases
  per type and focus the review there.
- Find valuable data by interviewing developers and users and reviewing source. Scanning with
  a tool such as ZAP, or exporting the entry point model from some WAFs, helps map web
  applications. Validate by walking through main use cases and following data and control
  flow.
- Prioritise remote entry points, especially anonymous public access: internet-facing code,
  web forms, files from outside the network, backward-compatible interfaces, custom APIs, and
  cryptography, authentication, authorisation and session code.
- Extra deployed versions, unused features and old backups enlarge the attack surface; backups
  are often ignored.
- Changes to the attack surface should trigger threat modelling and vice versa. Reassess when
  adding a different kind of interface, or changing authentication, session management,
  access control roles, encryption or secrets handling, validation, or architecture.
- Know whether the access model is deny-by-default (mistakes are easy to see) or
  allow-by-default (needs more care).
- For microservices, prioritise components reachable from an attack source; Cilium Hubble and
  kubeshark can help visualise the surface in Kubernetes and service meshes.

## Verify
- [ ] Each entry point, exit point, asset and trust level has a stable ID.
- [ ] Entry points and assets cross-reference trust levels.
- [ ] The map is compared with scanner or inventory output and updated when the design changes.

## Checked
Confirmed 2026-11-09 against the OWASP Threat Modeling Process page (external dependencies, entry points, exit points, assets and trust levels sections, fields and examples) and the OWASP Attack Surface Analysis cheat sheet (read in full), from local text copies.
Removed as unconfirmed: the sample entry point table, the route-table commands (`rails routes`, actuator `mappings`, `ss -lntp`), the classification advice for assets, the trust level role list, the pair-by-pair elevation-of-privilege rule and the "count matches inventory" check as stated.
Method: docs-checked 2026-11-09 against owasp.org Threat_Modeling_Process and cheatsheetseries.owasp.org Attack_Surface_Analysis_Cheat_Sheet
