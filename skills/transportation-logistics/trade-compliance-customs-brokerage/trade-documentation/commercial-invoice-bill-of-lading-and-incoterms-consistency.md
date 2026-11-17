---
id: transportation-logistics.trade-compliance-customs-brokerage.trade-documentation.commercial-invoice-bill-of-lading-and-incoterms-consistency
name: commercial-invoice-bill-of-lading-and-incoterms-consistency
category: transportation-logistics
field: trade-compliance-customs-brokerage
product: trade-documentation
tags: [trade-documentation, commercial-invoice, proforma-invoice, packing-list, bill-of-lading, b-l, house-bill, master-bill, sea-waybill, telex-release, air-waybill, awb, incoterms, incoterms-2020, exw, fca, fob, cif, dap, ddp, letter-of-credit, ucp-600, document-set, shipping-documents, export-documentation]
level: practitioner
status: gated
description: "Producing a consistent export document set: commercial invoice fields, packing list, bill of lading types and release, choosing and applying Incoterms 2020, and cross-checking before cargo moves."
sources: ["https://www.ecfr.gov/current/title-19/section-141.86", "https://iccwbo.org/business-solutions/incoterms-rules/", "https://iccwbo.org/news-publications/policies-reports/ucp-600/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commercial invoice, bill of lading and Incoterms consistency

**Goal:** issue documents that agree with each other and with the deal, so cargo clears
customs, the bank pays under a letter of credit, and nobody is stuck with costs they
didn't agree to.

## 1. Commercial invoice — must-haves
Seller and buyer (and consignee if different) with full addresses and tax/EORI IDs;
invoice number and date; **Incoterm with named place** ("FCA Rotterdam terminal X,
Incoterms 2020"); currency; for each line: description precise enough to classify
(material, function, model), HS code, country of origin, quantity and unit, unit
price, line total; total value; payment terms; packages count and gross/net weight;
marks and numbers; signature/declaration where required. US entries need additional
details per 19 CFR 141.86 (e.g. port of entry, itemised charges, rebates and bounties, discounts, assists).
- Separate freight/insurance on the invoice when the term includes them — needed for
  valuation.
- "No commercial value" samples still need a value for customs.

## 2. Packing list
Per package: number, contents, quantity, net/gross weight, dimensions. Must match the
invoice line totals and the transport document's package count and gross weight.

## 3. Transport documents
- **Ocean bill of lading (B/L):** receipt, evidence of contract, and (if
  **negotiable/"to order"**) a document of title — whoever holds an original endorsed
  B/L can claim the cargo. Often issued in sets of 3 originals (gated: unconfirmed, source is paywalled or blocked); surrender one to
  release.
- **Sea waybill / express release / telex release:** non-negotiable; cargo released
  to the named consignee without originals — faster, but no title control.
- **House vs. master B/L:** forwarders issue house bills to shippers; the carrier issues
  the master to the forwarder. Customs filings must reference the right one.
- **Air waybill (AWB):** always non-negotiable; consignee named.
- Clean B/L = no clauses about damaged goods; a "claused" B/L can block L/C payment.

## 4. Incoterms 2020 — choosing and applying
*The table summarises the ICC Incoterms 2020 rules (gated: unconfirmed, source is paywalled or blocked) The rules text is an ICC publication; confirm in the official rules.*
| Term | Risk passes | Main use |
|---|---|---|
| EXW | At seller's premises, not loaded | Domestic or very experienced buyers; buyer handles export clearance (often impractical) |
| FCA | On delivery to buyer's carrier at named place | **Default for containers** and most multimodal |
| FOB / CFR / CIF | Goods on board vessel at port of loading | **Bulk/break-bulk ocean**, not containers |
| CPT / CIP | On handover to first carrier; seller pays to destination | Multimodal; CIP requires all-risks (ICC A) insurance |
| DAP / DPU | At destination, ready for unloading / unloaded | Seller carries transport risk |
| DDP | At destination, import duties paid by seller | Seller needs import registration in buyer's country |
Always name the **precise place**. Incoterms do **not** transfer title or set payment.

## 5. Cross-check before release
Line-by-line: invoice ↔ packing list ↔ B/L/AWB ↔ L/C (if any) ↔ export declaration.
Check: shipper/consignee names identical, package count, gross weight, description
consistent (the L/C may require its exact wording), ports/places match the Incoterm,
dates (shipment date within L/C latest shipment date; presentation within the period stated in the credit (gated: unconfirmed, source is paywalled or blocked) UCP 600 is an ICC publication behind a paywall).

## Gotchas
- Using FOB for containers: risk stays with seller at the terminal while goods are out
  of their control — use FCA.
- Under L/Cs, banks check documents only; tiny discrepancies (spelling, weight)
  delay payment and incur fees.
- Vague descriptions ("parts", "gift", "samples") cause holds.
- *L/C presentation and invoice rules vary by bank and country; check the credit terms.*

## Verify
- [ ] Incoterm stated with version and precise named place on every document.
- [ ] Package count and gross weight identical on invoice, packing list and transport document.
- [ ] Descriptions classifiable and consistent across documents (and with the L/C wording).
- [ ] B/L type (negotiable vs. waybill) matches payment security needs.

## Checked

Jurisdiction: US invoice rules (19 CFR 141.86); Incoterms 2020 and UCP 600 are international ICC rules. Checked 2026-10-25: 141.86(a) lists port of entry, sale details, description, quantities, price, currency, itemised charges (freight, insurance, commission, containers, packing), rebates/bounties, country of origin and assists, and (g) covers discounts. Incoterms 2020, UCP 600 and bill-of-lading set practice are ICC or trade practice and were not confirmed (paywalled); marked gated.

Method: documentation only; no commands were run.
