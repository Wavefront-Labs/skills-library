---
id: engineering-technology.electrical-engineering.etap.etap-short-circuit
name: etap-short-circuit
category: engineering-technology
field: electrical-engineering
product: etap
tags: [ansi-c37, electrical-engineering, etap, etap-ansi-vs-iec-method, etap-duty-reports, etap-fault-study, etap-short-circuit, short-circuit-study]
level: practitioner
status: draft
description: "Run an ETAP short-circuit study: choose ANSI or IEC method, set fault locations and read device duty reports."
sources:
  - "https://etap.com/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# ETAP short-circuit study

1. **Choose the standard:** ANSI/IEEE (C37 series) for North American practice, IEC 60909 for IEC practice. The calculation method, voltage factors and breaker duty definitions differ, so select the one matching the equipment ratings.
2. **Study cases:** set a maximum-fault case (all sources, motors contributing) for equipment duty and a minimum-fault case (smallest source, motor contribution off, higher conductor temperature) for protection sensitivity.
3. **Fault types:** 3-phase, line-to-ground, line-to-line and double line-to-ground at selected buses; the 3-phase value generally governs interrupting duty, the line-to-ground value may govern near solidly grounded transformers.
4. **Reports:** bus fault current summaries, branch contributions, device duty comparisons (interrupting, momentary/close-and-latch, withstand), with alerts where duty exceeds rating.
5. **Review:** check the X/R used (high X/R reduces breaker rating with DC offset), motor contribution assumptions, and transformer taps.
6. Export results for the arc-flash and coordination studies, which depend on the same model.

**Tool-detail caveat:** menu names and report fields below are described from general ETAP practice and the ETAP documentation structure; confirm exact labels and options in the installed ETAP version's help (status draft, tool behaviour not re-run for this entry).

**Verify:** hand-check one bus with `Isc = MVA / (sqrt(3) kV)` for the dominant source and compare.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
