---
id: business-finance.procurement-and-supply-management.eprocurement-platforms.running-an-e-sourcing-event
name: running-an-e-sourcing-event
category: business-finance
field: procurement-and-supply-management
product: eprocurement-platforms
tags: [procurement-and-supply-management, eprocurement-platforms, e-procurement, e-sourcing, sap-ariba, ariba, coupa, jaggaer, sourcing-event, rfx, rfp, rfq, reverse-auction, e-auction, supplier-onboarding, supplier-enablement, catalogue, catalog, sourcing-template, award, procurement-software, s2p, source-to-pay]
level: practitioner
status: draft
description: "Set up and run an e-sourcing RFx or reverse auction in a procurement suite: supplier enablement, structured line items, scoring, rules, Q&A, award and hand-off."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running an e-sourcing event in a procurement suite

**Goal:** set up and run an RFx or reverse auction inside a procurement platform
(SAP Ariba Sourcing, Coupa Sourcing, Jaggaer and similar) so bids arrive structured,
comparable and auditable — and award flows into the contract and PO.

*Draft: describes the shared concepts across suites. Menu names, event types and
settings differ by product and version, and by how your administrators configured
them — confirm in your tenant's help and with your platform admin before a live event.*

## 1. Before you build
- Requirements, evaluation criteria and weights agreed offline first (see
  business-finance.procurement-and-supply-management.strategic-sourcing.rfp-design-and-weighted-evaluation).
- Check every invited supplier **exists and is enabled** in the platform's supplier
  directory with the right contact. Onboarding new suppliers (registration,
  qualification questionnaires, tax/bank details) can take days — start early.
- Pick the **event type**: RFI, RFP/RFQ (sealed bid), or **reverse auction** (live
  price competition). Use auctions only for well-specified items with enough
  competitors (rule of thumb ≥3) and where price is the main differentiator.
- Start from an organisational **template** where one exists — templates carry the
  approved legal terms, questionnaires and approval steps.

## 2. Build the event
- **Content:** sections of questions (yes/no, multiple choice, numeric, attachments)
  and **line items** with quantities and units. Structure pricing so the platform can
  total it; avoid "attach your price sheet" which kills automatic comparison.
- **Required vs optional** questions and **knockout/gating** questions for must-haves.
- **Scoring:** enable weighted scoring if available; assign questions to evaluation
  teams; price can be hidden from technical evaluators.
- **Rules:** timeline (preview period, open, close, Q&A cut-off), sealed vs visible
  bids, whether suppliers can revise, currency, auction format (rank vs price
  visibility, bid decrement, overtime/extension when late bids arrive).
- Attach documents: specifications, draft contract, NDA if needed.
- Route for **internal approval** if your workflow requires it before publish.

## 3. Publish and manage
- Run a **test event** or preview as a supplier for complex/auction events.
- Supplier briefing for auctions: rules, a practice session, what happens if their
  connection drops.
- Answer Q&A through the platform's message board so all suppliers see answers.
- Monitor participation: who has accepted, who hasn't opened it — chase early.

## 4. Evaluate and award
- Use the platform's side-by-side comparison and scoring; export to spreadsheet only
  for analysis, keeping the platform as the record.
- Run further rounds or a negotiation round if needed.
- **Award** in the platform: record the award decision and rationale; notify
  unsuccessful suppliers.
- Hand off to contract (contract workspace) and create **catalogue** or contract-backed
  buying channels so requisitions use the awarded prices.

## Gotchas
- **Wrong supplier contact** = no bid. Confirm contacts by phone before launch.
- Line items with inconsistent units of measure (box vs each) break comparison.
- Auctions ending at a fixed time without overtime rules invite last-second sniping.
- Changing an event after publish may require re-acknowledgement by all suppliers.
- Data protection: don't paste personal data into supplier-visible fields.

## Verify
- [ ] All invited suppliers registered, enabled and contact confirmed.
- [ ] Pricing captured as structured line items; units consistent.
- [ ] Timeline, sealed/visible rules and auction overtime settings checked in preview.
- [ ] All Q&A answered through the platform to every bidder.
- [ ] Award and rationale recorded in-platform and handed to contract/catalogue.
