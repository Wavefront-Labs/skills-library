---
id: engineering-technology.electrical-engineering.electrical-installation-design.switchboard-design
name: switchboard-design
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [busbar-rating-and-short-circuit, electrical-engineering, electrical-installation-design, form-of-separation, icw, iec-61439, rated-diversity-factor, switchboard-design, switchgear-assembly, ul-891]
level: advanced
status: draft
description: "Design LV switchboards to IEC 61439: busbar rating, short-circuit withstand, forms of separation and temperature rise verification."
sources:
  - "https://www.iec.ch/"
  - "https://www.nfpa.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Switchboard and switchgear assembly design

1. **Rated data:** rated voltage (Ue, Ui), rated current of the assembly (InA), of circuits (InC), rated diversity factor (RDF), rated short-time withstand current (Icw, 1 s or 3 s) and rated peak withstand (Ipk).
2. **Busbars:** size for design current including RDF; check temperature rise at the busbar joints; check short-circuit forces on supports using peak current `Ipk = n Icw` with factor `n` from IEC 61439-1 Table 7 (values depend on the power factor of the fault).
3. **Verification by design rules:** IEC 61439-1 allows verification by testing, calculation or design rules; use only a manufacturer's original system verification.
4. **Forms of separation (Form 1 to 4):** increase segregation of busbars, functional units and terminals; choose per maintainability and safety.
5. **Protective devices:** short-circuit rating Icc of the assembly must meet or exceed prospective fault current at the point of installation, or be protected by a current-limiting upstream device.
6. **IP and IK ratings**, creepage and clearance, internal arc classification (IEC TR 61641) where required, and ventilation.
7. **North America:** UL 891 switchboards, NEC 408 and 110.24 field marking of available fault current.

**Verify:** obtain the verification report and nameplate; check the assembly's Icw against the study.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
