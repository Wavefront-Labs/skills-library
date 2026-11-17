---
id: computing-software.email-administration.mail-server-administration.dmarc-record-policy
name: dmarc-record-policy
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dmarc-record-policy, dmarc, dmarc-record, p-reject, pct]
level: practitioner
status: docs-checked
description: "Publish a DMARC record at _dmarc with p=none, then quarantine, then reject, using rua reports and pct to roll out safely."
sources:
  - https://www.rfc-editor.org/rfc/rfc7489
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dmarc record policy

**Goal:** tell receivers what to do with mail failing alignment (RFC 7489).
## Steps
1. Start with monitoring: `_dmarc.example.com. TXT "v=DMARC1; p=none; rua=mailto:dmarc@example.com"`.
2. After reports show all legitimate sources aligned, move to `p=quarantine; pct=25`, raise `pct` stepwise, then `p=reject`. The `pct` tag (0 to 100, default 100) exists to allow a slow rollout of enforcement.
3. The `p` policy applies to the domain and its subdomains unless you set `sp=` for subdomains.
4. Make sure SPF or DKIM passes AND aligns with the From domain.
## Failure modes
- Moving to reject before inventorying third-party senders.
- Reports sent to an address in another domain need an authorization TXT record `example.com._report._dmarc.<reporting-domain>` with at least `v=DMARC1`.
- `pct` is not applied to DMARC-generated reports.
## Verify
- `dig +short TXT _dmarc.example.com` returns the record.

## Checked

2026-11-09. Confirmed on RFC 7489: the tag definitions for p, sp, pct (default 100, slow rollout purpose, not applied to reports), rua, the `p=none; rua=mailto:` and `pct=25` examples, and the external destination authorization record under _report._dmarc. Removed: the Authentication-Results check and the boilerplate Postfix/Dovecot notes.

Method: documentation only; no commands were run.
