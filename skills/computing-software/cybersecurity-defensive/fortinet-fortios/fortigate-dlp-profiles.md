---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-dlp-profiles
name: fortigate-dlp-profiles
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [dlp-sensor, fortios, dlp, data-leak-prevention, dlp-dictionary, fingerprint, sensitive-data]
level: practitioner
status: draft
description: "Configure FortiGate DLP using sensors or profiles, dictionaries and file patterns to detect sensitive data leaving the network."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: detect and block or log content such as card numbers or labelled documents.

FortiOS 7.2 and later reworked DLP into DLP profiles with `config dlp filepattern`, `config dlp dictionary` and filters; older releases use sensors. Confirm which model your version uses (`config dlp ?`).

```
config dlp dictionary
    edit "cards"
        set match-type match-any
        config entries
            edit 1
                set type "credit-card"
                set pattern "visa|mastercard"
            next
        end
    next
end
config dlp profile
    edit "dlp-std"
        config rule
            edit 1
                set name "block-cards"
                set proto smtp http-post
                set filter-by dictionary
                set dictionary "cards"
                set action block
            next
        end
    next
end
```
Attach it in the firewall policy. Dictionaries, regular expressions, file types, file size and document fingerprinting can be combined.

Gotchas
- DLP needs proxy-mode inspection for most protocols; flow-mode support is limited.
- HTTPS content is invisible without deep inspection.
- Regex false positives are common; start with `log-only` actions and review for a week.

## Verify
Create a test message in a lab with fake sample data (never real card numbers) and check the DLP log under Log & Report for a matching entry.
