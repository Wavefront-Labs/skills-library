---
id: computing-software.digital-forensics-incident-response.incident-response-process.sharing-incident-information-with-tlp-2
name: sharing-incident-information-with-tlp-2
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [traffic-light-protocol, tlp, information-sharing, need-to-know, incident-communications, dfir]
level: practitioner
status: docs-checked
description: "Label and handle incident information with FIRST TLP 2.0 (RED, AMBER, AMBER+STRICT, GREEN, CLEAR): who may receive it, how to mark messages and documents, and re-sharing rules."
sources: ["https://www.first.org/tlp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing incident information with TLP 2.0

TLP version 2.0 is the current FIRST standard, authoritative from August 2022. It indicates the sharing boundaries recipients must apply. FIRST states it is not a formal classification scheme, was not designed for licensing terms, handling or encryption rules, and does not affect freedom of information laws.

## Labels (FIRST definitions)
| Label | Recipient may share with |
|---|---|
| `TLP:RED` | Individual recipients only, no further disclosure; in a meeting, limited to those present |
| `TLP:AMBER+STRICT` | Only the recipient's own organisation (the source must specify it to restrict to the organisation only) |
| `TLP:AMBER` | Their organisation and its clients, on a need-to-know basis |
| `TLP:GREEN` | Peers and partner organisations within their community, not via publicly accessible channels, not outside the community |
| `TLP:CLEAR` | The world, no limit on disclosure, subject to standard copyright rules |

When "community" is not defined, assume the cybersecurity/defence community. Clients are by default included in TLP:AMBER so that recipients can pass information downstream for clients to protect themselves. FIRST defines a client as a person or entity that receives cybersecurity services from an organisation.

## Marking
- Written labels must not contain spaces and should be in capitals; labels stay in their original form even when content is translated.
- Messages (email, chat): the label and any extra restrictions go directly before the information, and the label should be in the email subject line. Mark where the labelled text ends if needed.
- Documents: the label and any extra restrictions in the header and footer of each page; 12-point type or greater for low-vision readers; right-justifying is recommended.
- Colour coding for sources to follow is in the standard (for example TLP:RED font #FF2B2B on a #000000 background).
- Use in automated exchanges (FIRST names MISP and IEP as examples) is left to the designers of the exchange but must follow the standard.

## Responsibilities
- The source is responsible for making sure recipients understand and can follow TLP.
- The source may add sharing restrictions; recipients must adhere to them.
- To share more widely than the label allows, the recipient must get explicit permission from the source. You cannot raise or lower someone else's label yourself.
- TLP can be used together with the Chatham House Rule but is distinct from it.

## Applying it during an incident (practice, not part of the standard)
- Pick the narrowest label that still lets recipients act. Information whose wider sharing would risk privacy, reputation or operations suits RED or AMBER (FIRST's own guidance for when to use these).
- Keep a distribution list per incident and record who received what in the comms log, so you can show recipients stayed within the label.

## Verify
Every outbound incident artefact carries a TLP label in the form above, and nothing marked RED or AMBER+STRICT is outside its permitted audience.

## Checked
Dated 2026-11-08. Confirmed against FIRST "Traffic Light Protocol (TLP) Standards Definitions and Usage Guidance, Version 2.0" at first.org/tlp: label meanings, community/organisation/clients definitions, marking rules, responsibilities, Chatham House note. Removed: the CISA page (blocked, 403 on fetch), the WHITE-to-CLEAR mapping, STIX 2.1 and MISP tag syntax, the "slide on every slide" rule, and per-scenario label assignments presented as fact (kept only as practice).
Method: docs-only read of cited pages, 2026-11-08
