---
id: computing-software.cybersecurity-defensive.threat-intelligence.misp-taxonomies-and-galaxies
name: misp-taxonomies-and-galaxies
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [misp-taxonomies, misp, misp-galaxies, tlp, tagging, threat-intelligence-platform, attack-mapping]
level: practitioner
status: docs-checked
description: "Apply MISP taxonomies and galaxies consistently: TLP/PAP and admiralty tags, local taxonomies, galaxy clusters for actors and ATT&CK, and enforcing tagging rules."
sources: ["https://www.misp-project.org/taxonomies.html", "https://www.misp-project.org/galaxy.html", "https://github.com/MISP/misp-taxonomies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MISP taxonomies and galaxies

## Taxonomies (machine tags)
Namespace:predicate="value" tags from the misp-taxonomies repo, e.g.
- `tlp:amber`, `tlp:amber+strict`, `PAP:GREEN`
- `admiralty-scale:source-reliability="b"`, `admiralty-scale:information-credibility="2"`
- `estimative-language:likelihood-probability="likely"`
- `circl:incident-classification="malware"`, `veris:...`, `kill-chain:Delivery`
- `workflow:state="complete"` for analysis status
Enable the taxonomies you need and keep them updated from the misp-taxonomies repo. Decide which tags are
mandatory (for example a TLP tag) and check your MISP version's documentation for how to enforce them.
Local taxonomy: create a JSON taxonomy for internal labels (business units, internal case IDs) and
load it rather than free-text tags.

## Galaxies (clusters with metadata)
- Threat actors (`misp-galaxy:threat-actor="APT29"`), MITRE ATT&CK patterns/groups/software, malware
  families (malpedia), tools, sectors, countries, ransomware groups.
- Attach clusters to events or attributes; relationships between clusters (synonyms, `uses`).
- Custom galaxies via the galaxy editor for internal actor clusters (with synonyms mapping to public names).

## Conventions
- Event-level: TLP, distribution-aligned tags, actor/malware galaxy, sector, confidence.
- Attribute-level: ATT&CK technique where precise, `to_ids` decisions, local tags for detection status.
- Document a tagging standard; avoid free-text tags (tag sprawl breaks search and exports).

## Gotchas
- Tags vs distribution: TLP tags inform humans; MISP distribution settings control sharing. Keep them consistent.
- Galaxy updates rename clusters; refresh galaxies regularly.

## Verify
Query events published last month without a TLP tag or actor/malware attribution: result should be empty
(or justified); tag list has no near-duplicate free-text tags.

## Checked
2026-10-28. Confirmed on the MISP taxonomies and galaxy pages and the misp-taxonomies repo: the tlp, PAP, admiralty-scale, estimative-language, kill-chain and veris namespaces and the threat-actor and ATT&CK galaxies. Removed: the Event Actions menu path, the tag collections and `required` setting claim, and the Galaxies > Update menu path.
Method: documentation only; no commands were run.
