---
id: computing-software.email-administration.mailcow.mailcow-mta-sts-policy
name: mailcow-mta-sts-policy
category: computing-software
field: email-administration
product: mailcow
tags: [mta-sts, mail-tls-policy, mta-sts-mode, dns-txt, policy-id, dane]
level: advanced
status: docs-checked
description: "Enable MTA-STS per domain in the mailcow UI (version 2025-09 or newer) with the matching _mta-sts TXT and mta-sts CNAME records."
sources: ["https://docs.mailcow.email/post_installation/setup-mta-sts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Setting up MTA-STS in mailcow

Requires mailcow 2025-09 or newer. mailcow now serves the policy dynamically from PHP and does not create files under `.well-known`; any manually created MTA-STS files from earlier setups become unreachable. MTA-STS is most useful for domains that cannot use DANE; with DANE it is optional extra protection.

UI: as admin go to E-Mail, Configuration, Domains, edit the domain and open the MTA-STS tab. Options: Version (only STSv1 exists), Mode (`none` for monitoring only, `testing` logs violations, `enforce` blocks them), Maximum Age (seconds; 86400, one day, is recommended) and MX entries (comma separated hosts allowed to receive mail). Tick Active and save.

DNS:
- TXT at `_mta-sts.yourdomain.tld` with `v=STSv1; id=2024090101`. The id must change whenever the policy changes; mailcow generates a new id on each save, and the blue DNS Check button in the UI shows the current one.
- CNAME at `mta-sts.yourdomain.tld` pointing to the mailcow FQDN, which lets a valid certificate be issued and sending servers fetch the centrally hosted policy.

Wait for propagation and use the DNS Check to confirm both records.

## Checked

2026-11-09. Confirmed on the MTA-STS page (raw markdown in the mailcow docs repo): 2025-09 requirement, dynamic PHP policy with no .well-known files, DANE note, UI path and options, modes, 86400 recommendation, TXT and CNAME records, id regeneration and DNS Check. No changes needed.

Method: docs-checked 2026-11-09 against the full MTA-STS page (setup-mta-sts.en.md in mailcow-dockerized-docs).
