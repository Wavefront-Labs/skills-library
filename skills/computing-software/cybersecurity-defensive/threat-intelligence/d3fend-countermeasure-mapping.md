---
id: computing-software.cybersecurity-defensive.threat-intelligence.d3fend-countermeasure-mapping
name: d3fend-countermeasure-mapping
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [mitre-attack, d3fend, countermeasure-mapping, defensive-techniques, control-coverage, digital-artifacts]
level: advanced
status: docs-checked
description: "Map defensive controls to MITRE D3FEND techniques and relate them to ATT&CK techniques to show which attack techniques each control may counter; treat the mappings as hypotheses."
sources: ["https://d3fend.mitre.org/", "https://d3fend.mitre.org/technique/d3f:ExecutableAllowlisting/", "https://d3fend.mitre.org/technique/d3f:ProcessSpawnAnalysis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping defences with D3FEND

**Goal:** a control inventory expressed in D3FEND terms, connected to the ATT&CK techniques it may counter, so gaps and overlaps are visible.

## D3FEND structure
- Seven tactics: Model, Harden, Detect, Isolate, Deceive, Evict, Restore.
- Techniques with ids, e.g. `D3-EAL` Executable Allowlisting (using a digital signature to authenticate a file before opening) and `D3-PSA` Process Spawn Analysis (analysing spawn arguments or attributes of a process to detect unauthorised ones).
- The ontology has a Digital Artifact class; technique pages list related ATT&CK techniques and offer an ATT&CK Navigator layer. The site states these ATT&CK mappings are "inferred, experimental, and will improve as the knowledge graph grows".

## Procedure
1. List deployed controls with configuration detail (e.g. "allowlisting enforced on servers", "process creation events forwarded to SIEM", "MFA for VPN").
2. Map each control to D3FEND techniques using the D3FEND site; look up each technique's page for its related ATT&CK techniques.
3. Build a matrix: priority ATT&CK technique (from your threat profile) x deployed D3FEND techniques, marking by D3FEND tactic.
4. Gaps = priority techniques with no Detect and no Harden coverage; overlaps = many controls on one technique (possible consolidation).

## Gotchas
- The mappings show what a defensive technique could counter, not that your implementation does; validate with adversary emulation before claiming coverage.
- Keep mappings versioned; D3FEND and ATT&CK both evolve (the ATT&CK tactic list shown on D3FEND pages already differs from older matrices).

## Verify
- [ ] Every critical control has D3FEND mappings with implementation notes.
- [ ] Coverage claims for top techniques are backed by a test result.

## Checked
2026-11-01. Confirmed on d3fend.mitre.org: the seven tactics, D3-EAL and D3-PSA names, ids and definitions, ATT&CK-related-technique lists and the "inferred, experimental" statement. Removed: D3-PSEP, D3-MFA, D3-NTA, D3-FE ids, NIST SP 800-53 mapping claims, the worked PowerShell example and the tactic assignment of D3-EAL (the page does not state a tactic).
Method: documentation only; no commands were run.
