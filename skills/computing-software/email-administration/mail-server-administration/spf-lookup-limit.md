---
id: computing-software.email-administration.mail-server-administration.spf-lookup-limit
name: spf-lookup-limit
category: computing-software
field: email-administration
product: mail-server-administration
tags: [spf-lookup-limit, spf-10-lookup-limit, spf-flattening, permerror]
level: advanced
status: docs-checked
description: "Stay under SPF's 10 DNS-lookup limit: count include, a, mx, ptr, exists and redirect, and flatten safely."
sources:
  - https://www.rfc-editor.org/rfc/rfc7208
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spf lookup limit

**Goal:** avoid `permerror` from too many lookups (RFC 7208 section 4.6.4).
## Steps
1. Count the terms that cause DNS queries: the include, a, mx, ptr and exists mechanisms and the redirect modifier. The limit is 10 in total during one evaluation; exceeding it must return `permerror`. The all, ip4, ip6 mechanisms and the exp modifier are not subject to the limit.
2. An `mx` mechanism also must not cause more than 10 address (A or AAAA) lookups for its MX records, or it returns `permerror`.
3. Void lookups (a positive answer with no records, or a name error) should be limited to two; exceeding that gives `permerror`.
4. Reduce: replace `a`/`mx` with `ip4:`/`ip6:`, drop vendors you no longer use, and do not publish `ptr` (the RFC says it SHOULD NOT be published).
5. If you flatten includes into addresses, automate it, since the addresses you copied can change on the vendor side.
## Failure modes
- A vendor adds nested includes and pushes the evaluation over the limit.
- A `permerror` means the published records could not be correctly interpreted; receivers cannot get an authorization result from them.
## Verify
- Use an SPF evaluator of your choice and confirm the count of lookup-causing terms (including nested ones) is 10 or fewer and void lookups are 2 or fewer.

## Checked

2026-11-09. Confirmed on RFC 7208: section 4.6.4 (terms that cause DNS queries, limit of 10 with permerror, exp/all/ip4/ip6 exempt, the 10 address-record limit for mx, void lookups limited to two with permerror) and section 5.5 (ptr SHOULD NOT be published). Removed: the DMARC consequence, the named tools spfquery and pyspf, and the generic Postfix/Dovecot notes, which the RFC does not cover.

Method: documentation only; no commands were run.
