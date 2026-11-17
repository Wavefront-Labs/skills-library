---
id: computing-software.systems-network-administration.dns-dhcp.registrar-domain-transfer
name: registrar-domain-transfer
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, domain-transfer, epp-code, registrar, icann-transfer-policy]
level: practitioner
status: docs-checked
description: "Transfer a domain between registrars safely: unlocking, EPP auth codes, ICANN 60-day locks, keeping DNS up and DNSSEC during the move."
sources:
  - https://www.icann.org/resources/pages/transfer-policy-2016-06-01-en
  - https://www.icann.org/resources/pages/name-holder-faqs-2017-10-10-en
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registrar domain transfer

Changing registrar (who manages the registration) is separate from changing DNS hosting. Done carelessly it causes outages.

## Preconditions (gTLDs, ICANN Transfer Policy)
- Registrars may deny a transfer request within 60 days of the domain's creation, and within 60 days after a previous inter-registrar transfer.
- After a Change of Registrant, a 60-day transfer lock applies unless the registrant opted out.
- Status must not be `clientTransferProhibited` (the registrar must remove it on request) or `serverTransferProhibited` (set by the registry; removal goes through the registrar to the registry and takes longer).
- A valid registrant email: the transfer authorisation goes to the registrant.
- Check status with your registrar's control panel or an RDAP lookup (see domain-expiry-monitoring).

## Steps
1. (Practitioner advice) Make sure DNS does not depend on the losing registrar: if their name servers host the zone, move DNS hosting first or confirm the zone keeps being served after transfer.
2. Get the Auth-Code (AuthInfo, EPP or transfer code) from the losing registrar. The name-holder FAQ says the registrar must provide it within five calendar days of request; many registrars offer self-service generation.
3. Start the transfer at the gaining registrar, supplying the Auth-Code.
4. Respond to the authorisation emails. Under the policy, if the Registrar of Record does not respond within 5 calendar days the transfer is approved by default; the initial form of authorisation expires after 60 days. ICANN has deferred compliance enforcement of the policy's FOA requirement (Board resolution of 26 January 2020), so the email flow may differ between registrars.
5. (Practitioner advice) After completion, re-check name servers, DS records, contacts, auto-renew and re-enable the registrar lock (`clientTransferProhibited`).
6. If a transfer is stuck or disputed, the policy defines a Transfer Emergency Action Contact (TEAC) channel between registrars and the Transfer Dispute Resolution Policy; ask the gaining registrar to escalate.

ccTLDs follow their own registry policies, not the ICANN gTLD Transfer Policy; check the registry's rules.

## DNSSEC (practitioner advice)
If the losing registrar's DNS hosting signs the zone, the DS record at the registry points to keys you lose on transfer. Remove the DS before moving, or migrate signing first so the chain stays valid.

## Verify
- [ ] RDAP shows the new registrar, NS and DS are unchanged or intentionally updated, and the lock status is restored.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the ICANN Transfer Policy page and the name-holder FAQ transfer answers (Auth-Code, 5 calendar days, 60-day denial reasons), and the ICANN EPP Status Codes page for transfer-prohibited statuses. Removed as unsupported: the whois|grep command, "adds one year", the .uk IPS tag and .de examples, and the RFC 8901 reference. The DNSSEC and post-transfer steps are practitioner advice.
