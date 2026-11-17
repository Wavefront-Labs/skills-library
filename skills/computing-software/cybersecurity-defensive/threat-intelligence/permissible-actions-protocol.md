---
id: computing-software.cybersecurity-defensive.threat-intelligence.permissible-actions-protocol
name: permissible-actions-protocol
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [pap, information-sharing, tlp, misp-taxonomies, ioc-handling, operational-security]
level: practitioner
status: docs-checked
description: "Use the Permissible Actions Protocol (PAP) alongside TLP: PAP levels, what each permits recipients to do with indicators, and applying PAP in MISP and sharing communities."
sources: ["https://www.misp-project.org/taxonomies.html#_pap", "https://github.com/MISP/misp-taxonomies/blob/main/PAP/machinetag.json", "https://www.first.org/tlp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Permissible Actions Protocol (PAP)

TLP tells recipients who they may share with; PAP tells them **what actions** they may take with the
information, mainly to avoid tipping off the adversary.

## Levels (MISP PAP taxonomy)
- **PAP:RED**: non-detectable actions only. Recipients may not use the information on the network; only
  passive actions on logs that are not detectable from the outside.
- **PAP:AMBER**: passive cross check. Recipients may run online checks with third-party services (the taxonomy
  gives ripe whois as an example) or set up a monitoring honeypot.
- **PAP:GREEN**: active actions allowed: ping the target, block incoming/outgoing traffic to or from it, or
  configure honeypots to interact with it.
- **PAP:CLEAR**: no restrictions. The MISP taxonomy still lists `PAP:WHITE` with the same meaning.

## Why it matters
Uploading a targeted sample to a public sandbox or visiting a C2 domain from your network can alert
the adversary that they were detected, burning an investigation or a partner's source.

## Applying PAP
- Tag events/attributes in MISP (`PAP:AMBER`); enforce in automation: exports to blocking controls only
  for PAP:GREEN/CLEAR; enrichment modules that query external services disabled for PAP:RED.
- State PAP in shared reports next to TLP ("TLP:AMBER, PAP:AMBER").
- Honour the strictest marking when combining sources.

## Gotchas
- Many analysts confuse TLP with PAP; train them.
- Retro-hunting in your own logs is a passive action (allowed even under PAP:RED); automated enrichment
  that contacts third-party services needs at least PAP:AMBER.

## Verify
Automation config shows PAP-aware filters; spot check that PAP:RED indicators never reached external
enrichment logs.

## Checked
2026-10-28. Confirmed in the MISP PAP machinetag.json (version 3, RED/AMBER/GREEN/CLEAR plus WHITE) and the FIRST TLP page (TLP:CLEAR is a current label). Rewrote the level descriptions to follow the taxonomy text; removed the claims about passive DNS, sandbox submission and sinkholing, which the taxonomy does not state.
Method: documentation only; no commands were run.
