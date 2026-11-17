---
id: computing-software.digital-forensics-incident-response.incident-response-process.investigating-vendor-impersonation-and-lookalike-domains
name: investigating-vendor-impersonation-and-lookalike-domains
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [lookalike-domain, bec, vendor-impersonation, typosquatting, dnstwist, dfir]
level: practitioner
status: docs-checked
description: "Investigate BEC vendor impersonation: spot lookalike domains, enumerate permutations with dnstwist, scope threads, report to the registrar, tune impersonation protection."
sources: ["https://github.com/elceef/dnstwist", "https://learn.microsoft.com/en-us/defender-office-365/anti-phishing-policies-about", "https://www.icann.org/resources/pages/abuse-2014-01-29-en"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Investigating vendor impersonation and lookalike domains

Classic BEC: the attacker compromises a supplier's mailbox, reads an invoice thread, then continues it from a lookalike domain (`acme-supplies.co` vs `acmesupplies.com`, `rn` for `m`, swapped TLD) asking for new bank details.

## Spot it in the message
- Compare From, Reply-To and Return-Path domains character by character; render them in a monospace font. Check for IDN/punycode (`xn--`). Microsoft's own example of domain impersonation is a lookalike with an accented character (ćóntoso.com for contoso.com).
- Thread hijack signs: the conversation history is real, but the new message comes from a different domain or the Reply-To changed mid-thread.
- Authentication: an impersonated domain can look legitimate (it is registered and has email authentication DNS records) while its intent is to deceive; passing SPF/DKIM for its own domain does not mean legitimate.

## Enumerate and enrich
```bash
dnstwist --registered --format csv acmesupplies.com > perms.csv
dnstwist --registered --lsh acmesupplies.com
```
- dnstwist generates permutations of the domain (including homoglyph and hyphenation fuzzers, IDN, optional
  dictionary files) and checks which are in use. `--registered` shows only registered ones; `--format` takes `csv`,
  `json` or `list` (`list` makes no DNS lookups); `--lsh` fetches live pages and compares an HTML fuzzy hash
  (ssdeep by default, TLSH optional) with the original; `--geoip` adds location; `--fuzzers` selects algorithms.
  It also lists rogue MX host detection among its features.
- For hits: WHOIS creation date (days before the email is a strong signal), registrar, MX records (mail-capable),
  certificate transparency logs for related names, and passive DNS for other domains on the same IP, using your own
  tooling for these.

## Scope
1. Search mail logs for all messages from and to the lookalike domain (message trace, or your mail-security
   product's email event table filtered on sender domain or recipient).
2. Identify every internal user who replied; those threads may contain further fraud attempts or leaked data.
3. Tell the genuine vendor through a known-good contact (phone from the master vendor file, not the email): their mailbox is probably compromised.
4. If payment was sent, start the wire-recall process immediately (time-critical).

## Respond
- Block the domain in mail flow and web proxy. In Defender for Office 365 anti-phishing policies, domain
  impersonation protection covers up to 50 custom domains per policy and user impersonation protection up to 350
  users; it checks other TLDs and slightly similar domains. Trusted senders and domains (up to 1,024 entries) are
  exceptions to impersonation protection, so keep the lookalike out of them. Note: with mailbox intelligence on,
  domain impersonation protection does not fire if sender and recipient previously communicated by email.
  These impersonation settings exist only in Defender for Office 365 policies, not in basic anti-phishing.
- Report to the registrar's abuse contact and the hosting provider with headers as evidence. ICANN states that
  accredited registrars (2013 RAA) must keep an abuse contact, investigate reports promptly, publish their abuse
  handling procedure and give an abuse address and phone in Whois results; law-enforcement reports should be reviewed
  within 24 hours. For brand abuse via the UDRP, use counsel (not covered by the cited pages).
- Proactively monitor dnstwist permutations of your own domain and key suppliers.

## Gotchas
- Free webmail display-name spoofing ("Acme Accounts <acme.ar@gmail.com>") is the same attack without a domain; check the address, not the name.
- Payment-change requests should always be verified out of band; the investigation should check whether that control was followed.

## Verify
All messages involving the lookalike domain are listed, each internal reply reviewed, and the domain is blocked at mail and web layers.

## Checked
2026-11-08. Confirmed on the dnstwist README: `--registered`, `--format` csv/json/list, `--lsh` with ssdeep/TLSH,
`--geoip`, `--fuzzers` and rogue MX detection; on the Microsoft anti-phishing page: the 50-domain, 350-user and
1,024-entry limits, TLD and similar-domain checks, the mailbox intelligence interaction and the Defender-only
availability; on the ICANN page: registrar abuse obligations. Removed: the `--mxcheck` and `--whois` options (not in
the README), crt.sh by name, the unreferenced IC3 source, and the UDRP specifics.
Method: documentation only; no commands were run.
