---
id: transportation-logistics.logistics-supply-chain.dangerous-goods-transport.dg-shipment-preparation
name: dg-shipment-preparation
category: transportation-logistics
field: logistics-supply-chain
product: dangerous-goods-transport
tags: [dangerous-goods-transport, dangerous-goods, hazmat, hazardous-materials, logistics-supply-chain, un-number, proper-shipping-name, hazard-class, packing-group, adr, imdg, imdg-code, iata-dgr, 49-cfr, dot-hazmat, sds, safety-data-sheet, segregation, marking-and-labelling, placarding, dg-declaration, limited-quantity, excepted-quantity, lithium-batteries, un-packaging]
level: practitioner
status: gated
description: "Prepare a dangerous-goods shipment: classify from the SDS, find the UN entry, pick the mode rulebook (ADR, IMDG, IATA, 49 CFR), package, mark, label, document and segregate."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DG shipment preparation — classify, pack, mark, document, segregate

**Goal:** ship hazardous materials legally and safely by road, sea or air. This is a
regulated activity: in most jurisdictions only **trained (and sometimes certified)**
staff may classify, pack or sign DG documents. Use this as a working method, and the
current edition of the rulebook as the authority.

## 1. Pick the rulebook for every leg
| Mode | Rule | Notes |
|---|---|---|
| Road (Europe + others) | ADR | Updated every 2 years (odd years) (gated: unconfirmed, source is paywalled or blocked) |
| Sea | IMDG Code | Amendment cycle every 2 years (gated: unconfirmed, source is paywalled or blocked) |
| Air | IATA DGR (based on ICAO TI) | New edition every 1 January; airline variations |
| US domestic | 49 CFR (PHMSA) | Parts 171–180 |
| Rail (Europe) | RID | Mirrors ADR |
A multimodal shipment must satisfy each leg; air is generally the strictest.

## 2. Classify
From the **Safety Data Sheet (SDS) section 14**, confirm (don't just copy — SDSs are
often wrong):
- **UN number** and **proper shipping name (PSN)** (add technical name in brackets for
  "N.O.S." entries).
- **Class/division** (1 explosives, 2 gases, 3 flammable liquids, 4 flammable solids,
  5 oxidisers/organic peroxides, 6 toxic/infectious, 7 radioactive, 8 corrosives,
  9 miscellaneous incl. lithium batteries) and subsidiary hazards.
- **Packing group** I (high), II (medium), III (low danger).
- Marine pollutant / environmentally hazardous?
Then look up the entry in the Dangerous Goods List of the relevant code: it gives
special provisions, quantity limits, packing instruction, and whether it's forbidden
(e.g. on passenger aircraft).

## 3. Choose the shipping regime
- **Fully regulated**, **limited quantity (LQ)** (small inner packagings, reduced
  requirements, LQ diamond mark), or **excepted quantity (EQ)** (tiny amounts).
- Check the quantity per inner and per package against the column limits.

## 4. Package
- Use **UN-specification packaging** tested for the packing group (marked e.g.
  `4G/Y25/S/...` — X = tested for PG I, II and III; Y = PG II and III; Z = PG III only, per 49 CFR 178.503) unless LQ/EQ.
- Follow the packing instruction exactly: inner packaging, absorbent, closures,
  orientation arrows for liquids, outer box.
- Lithium batteries: separate instructions for cells/batteries alone, packed with, or
  contained in equipment (UN3480/3481/3090/3091 all appear in 49 CFR 172.101 and 173.185, checked); state of charge limits for air (gated: unconfirmed, source is paywalled or blocked).

## 5. Mark and label
- Package: UN number + PSN, hazard labels (class diamond and subsidiary), orientation
  arrows, marine pollutant mark if applicable, shipper/consignee.
- Vehicle/container: placards and orange plates (ADR) or placards on four sides
  (IMDG containers) as required by quantity.

## 6. Document
- Dangerous goods declaration / transport document: UN number, PSN, class, PG,
  quantity and packaging, emergency contact, signed declaration by trained person.
  Air: Shipper's Declaration for Dangerous Goods. Sea: DG declaration + container
  packing certificate.
- Keep copies for the retention period of the rule.

## 7. Segregate and load
- Check the segregation table of the mode (e.g. IMDG "away from", "separated from";
  ADR mixed-loading prohibitions) — e.g. oxidisers away from flammables, acids from
  cyanides. Food and feed kept apart from toxics.
- Secure packages upright, no leaks; driver has written instructions (ADR) and required equipment.

## Gotchas
- Old edition used — check effective date every year.
- Airline/state variations can forbid what IATA allows.
- "Non-hazardous" on the SDS for one mode doesn't mean all modes (e.g. marine pollutants).
- Damaged returns of lithium batteries need special provisions.

## Verify
- [ ] UN/PSN/class/PG checked against the DG list, not only the SDS.
- [ ] Packaging spec mark matches PG and packing instruction.
- [ ] Marks/labels match the declaration exactly.
- [ ] Segregation checked for the whole load; signer is trained and in date.

*Uncertainty:* 49 CFR items above were checked on eCFR; ADR, IMDG and IATA edition details were not (paywalled or blocked). Not a specific edition; always confirm against the current regulation.
