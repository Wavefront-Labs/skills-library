---
id: computing-software.systems-network-administration.dns-dhcp.registry-lock-and-domain-hijacking
name: registry-lock-and-domain-hijacking
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns-security, registry-lock, domain-hijacking, registrar, epp-status, clienttransferprohibited, mfa]
level: practitioner
status: docs-checked
description: "Protect critical domains from hijacking: registrar account hardening, EPP client locks versus server locks, registry lock, monitoring and response."
sources:
  - https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry lock and domain hijacking

Anyone who controls the registrar account can change name servers or delegation data and so redirect web, email and certificate validation for the domain. Protect the account and add locks that an account compromise cannot remove alone.

## Registrar account hygiene (practitioner advice)
- Use role accounts with strong MFA and no shared passwords.
- Limit who can change name servers or DS records; use any change-approval feature your registrar offers.
- Keep the registrar contact mailbox on a different domain from the one being protected, monitored by a team.
- Keep a payment method that will not lapse and track expiry separately (see domain-expiry-monitoring).

## EPP status codes (ICANN)
Every domain has at least one EPP status code. Client codes are set by the registrar; server codes are set by the registry and take precedence over client codes. Both show in a Whois lookup.
- `clientTransferProhibited`, `clientUpdateProhibited`, `clientDeleteProhibited`: make the registry reject transfer, update or delete requests. ICANN suggests asking your registrar to enact them to help prevent unauthorised transfers, updates or deletions. To transfer, update or delete you must ask the registrar to remove the code.
- `serverTransferProhibited`, `serverUpdateProhibited`, `serverDeleteProhibited`: uncommon, usually set during legal disputes, at the registrant's request or during redemptionPeriod. Some registry operators offer a Registry Lock Service that lets registrants, through their registrars, set these as extra protection. Removing them takes longer than the client equivalents because the registrar has to forward the request to the registry and wait for it to lift the restriction.
- `pendingTransfer` means a transfer request is being processed; if you did not request it, contact the registrar immediately and ask them to deny it.

Apply a registry lock to domains whose loss would be severe (main corporate, mail and customer-facing domains) if your registrar and registry offer the service; availability and cost vary.

## Monitoring (practitioner advice)
- Compare the delegation (NS) and DS records published at the parent with what you expect on a schedule.
- Watch certificate transparency logs for unexpected issuance for your names.
- Send registrar notifications to a monitored mailbox.

## If hijacked
1. Contact the registrar immediately with proof of ownership; ask for restoration and a lock.
2. Revoke certificates issued during the window.
3. Rotate credentials that may have been captured through attacker-controlled mail or web.
4. Report it to the registry and, where relevant, a national CERT.

## Verify
- [ ] Critical domains show the intended client and server prohibited statuses, and NS/DS change alerts fire in a test.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the ICANN EPP Status Codes page in full. The CISA Emergency Directive 19-01 source returned 403 and was not read, so its claims and the source were removed. Removed as unsupported by ICANN: named registries and operators, the out-of-band phone-passphrase process, ccTLD and new gTLD support claims and the whois/dig commands. Hygiene, monitoring and incident steps are practitioner advice, not ICANN statements.
