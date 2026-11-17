---
id: energy-mining-utilities.telecommunications-network-operations.carrier-fraud-prevention.detecting-and-blocking-irsf-traffic
name: detecting-and-blocking-irsf-traffic
category: energy-mining-utilities
field: telecommunications-network-operations
product: carrier-fraud-prevention
tags: [carrier-fraud-prevention, telecommunications-network-operations, telecom-fraud, irsf, international-revenue-share-fraud, premium-rate-fraud, pbx-hacking, sip-fraud, wangiri, simbox, bypass-fraud, high-risk-ranges, hot-number-list, fms, fraud-management-system, cdr-analysis, velocity-rules, threshold-alerts, test-call-generation, blocking, barring, gsma, cfca, roaming-fraud, nrtrde, call-pattern-analysis]
level: practitioner
status: draft
description: "Spot and stop international revenue share fraud: the call patterns, high-risk number ranges, near-real-time CDR rules, blocking decisions and the evidence to keep for disputes."
sources: ["GSMA fraud and security group public materials (concepts, paraphrased)", "CFCA Global Fraud Loss Survey (public summaries)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detecting and blocking IRSF traffic

**Goal:** catch **international revenue share fraud (IRSF)** — fraudsters pumping calls
to expensive international or premium numbers they profit from — within minutes, not
on the monthly bill, and stop it without blocking legitimate customers. IRSF is
consistently reported among the costliest telecom fraud types (CFCA, GSMA).

## 1. How the fraud works
- Fraudster obtains numbers in a high-cost range (often small island nations,
  satellite ranges, or unallocated/hijacked ranges) from a "premium rate" provider who
  shares the termination revenue.
- They generate calls to those numbers through a channel they don't pay for:
  **hacked PBX / SIP accounts**, stolen or subscription-fraud SIMs, compromised
  roaming SIMs, or test numbers abused on your interconnect.
- Calls happen in bursts, often on weekends and nights when nobody is watching.
- The originating carrier must still pay the downstream carriers even if the
  customer won't pay.

## 2. Signals in the CDRs
Run near-real-time rules on call detail records (seconds-to-minutes delay, not daily):
- **Velocity:** many calls or minutes to international destinations from one
  account/trunk in a short window, especially one with no history of international
  calling.
- **Destination risk:** calls to ranges on a **high-risk number list** (industry hot
  lists and your own history). Watch for sequential B-numbers (…001, …002, …003).
- **Simultaneous calls** exceeding what the customer's trunk/plan ever uses.
- **Short repeated calls** of similar duration, or long calls of near-identical length
  (automated generation).
- **Off-hours** spikes from business PBXs.
- **Roaming:** NRTRDE (near-real-time roaming data exchange) records showing high-cost
  calls from inbound roamers.

## 3. Respond
1. **Confirm quickly**: check the pattern and the account's history. A business that
   just opened a branch abroad looks different from 300 calls to sequential numbers
   at 03:00.
2. **Block proportionately:**
   - destination block for the specific ranges at the switch/SBC;
   - account or trunk international barring;
   - full suspension only when needed.
3. **Contact the customer** by a known channel — for PBX hacking, they must change
   credentials and close the exposed SIP/voicemail ports.
4. **Preserve evidence:** CDRs, timeline, block actions. They support disputes with
   interconnect partners and withholding payment where agreements allow.
5. Feed newly found ranges into your hot list and share through industry channels
   where you participate.

## 4. Prevention
- Default international barring or credit/velocity limits on new and prepaid accounts.
- Fraud management system (FMS) rules tuned with feedback, not left at defaults.
- **Test call generation** campaigns to detect bypass (simbox) and confirm routing
  integrity on your interconnects.
- Customer PBX/SIP hardening advice: strong passwords, IP allow-lists, disable unused
  features.

## Gotchas
- Blocking whole countries harms legitimate customers and diaspora communities —
  block number ranges, not countries, unless the risk justifies it.
- Fraudsters move ranges quickly; a static hot list goes stale within weeks.
- Wangiri (one-ring callback scams) is related: inbound missed calls from premium
  ranges prompting callbacks — block or warn on callbacks to those ranges.
- Uncertain: thresholds depend heavily on customer type and market; the examples are
  patterns, not tuned values.

## Verify
- [ ] CDR rules run in near real time with velocity, destination-risk and concurrency checks.
- [ ] Hot list updated in the last few weeks.
- [ ] Each alert triaged against account history before blocking.
- [ ] Blocks are proportionate and logged; customer contacted by a known channel.
- [ ] Evidence package kept for disputes.
