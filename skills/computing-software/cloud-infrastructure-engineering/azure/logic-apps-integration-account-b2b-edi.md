---
id: computing-software.cloud-infrastructure-engineering.azure.logic-apps-integration-account-b2b-edi
name: logic-apps-integration-account-b2b-edi
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, logic-apps, integration-account, edi, b2b, as2, x12, edifact]
level: advanced
status: docs-checked
description: "Set up a Logic Apps integration account for B2B: partners, agreements, schemas, maps and certificates, and run AS2/X12/EDIFACT decode and encode workflows."
sources: ["https://learn.microsoft.com/azure/logic-apps/logic-apps-enterprise-integration-overview", "https://learn.microsoft.com/azure/logic-apps/logic-apps-enterprise-integration-create-integration-account", "https://learn.microsoft.com/azure/logic-apps/logic-apps-enterprise-integration-x12", "https://learn.microsoft.com/azure/logic-apps/logic-apps-enterprise-integration-as2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integration accounts and B2B EDI

**Goal:** exchange EDI documents with trading partners from Logic Apps.

## Integration account
- Resource holding **partners**, **agreements**, **schemas** (XSD), **maps** (XSLT/Liquid), **certificates**, and batch configs.
- Pick the integration account tier from the Logic Apps pricing and limits documentation (tier capabilities not confirmed here).
- Link it to a Consumption logic app (Workflow settings → Integration account), or for **Standard** logic apps add schemas and maps directly to the logic app resource; linking an integration account is required or optional depending on the scenario (for example X12 and AS2 operations need a link).

## Configure trading
1. **Partners**: host (your company) and guest, each with business identities.
2. **Agreements**: host + guest + protocol (AS2, X12, EDIFACT, RosettaNet), receive and send settings (envelopes, acknowledgements, validation, character sets).
3. **Certificates** for AS2 signing/encryption: public certificates for partners and your own private key as the docs describe.
4. **Schemas** for each transaction set and **maps** to your internal format.

## Inbound workflow (AS2 + X12)
Request trigger (partner posts AS2) → **AS2 Decode** (verify signature, decrypt, generate MDN) → respond with MDN (sync) → **X12 Decode** (split interchange, validate, generate acknowledgements) → Transform XML (map) → route to ERP. Outbound reverses: transform → **X12 Encode** → **AS2 Encode** → HTTP to partner.

## Monitoring
- Enable B2B tracking to Log Analytics to search messages by control number (check the current tracking docs).
- Alert on failed decodes and missing acknowledgements.

## Gotchas
- Control number uniqueness/duplicate checks are per agreement settings; replays may be rejected.
- Certificate expiry breaks AS2 silently for partners: track expiry dates.

## Verify
- [ ] Partner test interchange decoded, acknowledgement returned, map output validated against the internal schema.

## Checked

2026-10-28. Confirmed on the Logic Apps enterprise integration pages: X12 and AS2 operations need a link between the logic app and an integration account (Consumption and Standard), Standard logic apps can hold schemas and maps directly in the logic app resource. Removed: tier capability descriptions, the Artifacts folder name, example identity qualifiers, X12 transaction set numbers, acknowledgement codes, the Key Vault claim and the chunking advice (not found in fetched pages).

Method: documentation only; no commands were run.
