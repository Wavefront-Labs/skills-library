---
id: energy-mining-utilities.telecommunications-network-operations.intercarrier-settlement-porting.working-number-port-requests-and-rejects
name: working-number-port-requests-and-rejects
category: energy-mining-utilities
field: telecommunications-network-operations
product: intercarrier-settlement-porting
tags: [intercarrier-settlement-porting, telecommunications-network-operations, number-porting, number-portability, lnp, mnp, port-in, port-out, npac, lrn, loa, letter-of-authorisation, csr, customer-service-record, lsr, foc, firm-order-commitment, port-reject, jeopardy, snapback, port-out-fraud, sim-swap, routing-database, number-portability-administrator, porting-desk]
level: practitioner
status: draft
description: "Run a porting desk: validate a port request against the losing carrier's record, avoid the common rejects, schedule activation, handle jeopardies and snapbacks, and stop port-out fraud."
sources: ["US FCC number portability rules and NPAC/LNPA process concepts (public, paraphrased)", "Ofcom General Condition B3 porting concepts (UK)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Working number port requests and rejects

**Goal:** move a customer's telephone numbers from one carrier to another with no
loss of service, minimal rejects and no fraud. Porting sits between carriers and a
shared database (in the US, the **NPAC** run by the number portability
administrator; other countries use central or distributed databases). Terminology
below is mainly US; the workflow pattern is widespread. Timelines are regulated and
change — confirm current rules for your country and service type.

## 1. The flow (US wireline/VoIP example)
1. **Gaining carrier** gets a signed **letter of authorisation (LOA)** from the
   customer and, ideally, a recent bill or **customer service record (CSR)** from the
   losing carrier.
2. Gaining carrier submits a **port request** (an LSR for wireline; wireless uses its
   own inter-carrier interface).
3. **Losing carrier** validates and returns a **firm order commitment (FOC)** with
   the due date — or a **reject** with a reason.
4. Gaining carrier creates the subscription in the NPAC with its **LRN** (location
   routing number); on the due date it **activates**, and networks start routing to the
   new carrier.
Simple wireless ports in the US are expected to complete within about a business day;
wireline ports often take longer — confirm the current interval rules.

## 2. Validate before you submit — avoiding rejects
Most rejects are data mismatches. Compare the request to the CSR:
- **Account number** — the losing carrier's, not the customer's new one.
- **Name and service address** exactly as on the losing account (abbreviations matter).
- **PIN / passcode** (mandatory on most mobile ports).
- **Billing telephone number (BTN)** and all numbers on the account: porting some
  numbers off a hunt group or a main number without handling the rest is a frequent
  reject.
- **Authorised signer** on the LOA matches the account holder.
- Numbers not already in a pending port, not disconnected (some carriers can't port
  numbers that are already disconnected).

## 3. Handling rejects and jeopardies
- Read the reject code — it usually names the field. Fix and resubmit; don't resubmit
  unchanged.
- If the CSR conflicts with what the customer says, ask the customer for a recent
  bill — they often hold several accounts.
- **Jeopardy:** the due date is at risk (provisioning not ready, conflicting order).
  Communicate the new date to the customer before the old one passes.

## 4. Activation day
- Make sure your switch/softswitch or platform has the numbers built and routing
  tested *before* activation.
- Activate in the database, then place test calls in from another network and out
  from the ported numbers. Check SMS and emergency (E911/999) address records.
- **Snapback:** if activation went wrong, the porting process may allow a quick return
  to the old carrier — know your procedure and deadlines.

## 5. Port-out fraud
Criminals port a victim's mobile number to take over bank and email accounts.
- Enforce the account PIN; never give a customer's PIN or account number over the
  phone to an unverified caller.
- Flag ports on accounts with recent SIM change or credential changes; notify the
  customer by an existing channel.
- Support customer-set port freezes/locks where offered.

## Gotchas
- A partial port leaves the remaining numbers on a separate account with the old
  carrier — tell the customer, or they keep paying.
- Toll-free numbers port through a different system (in the US, the toll-free
  administrator), not the LNP process.
- Uncertain: forms, field names, intervals and fraud rules differ by country, service
  type and inter-carrier agreements.

## Verify
- [ ] LOA signed by the account holder; CSR or recent bill obtained.
- [ ] Account number, name, address, PIN and all numbers match the losing record.
- [ ] FOC received and due date confirmed with the customer.
- [ ] Routing built and tested before activation; test calls and emergency address checked after.
- [ ] Fraud flags checked before any port-out completes.
