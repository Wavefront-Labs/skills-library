---
id: computing-software.systems-network-administration.coredns.coredns-template-plugin
name: coredns-template-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, template, go-template, dynamic, response]
level: advanced
status: docs-checked
description: "Generate DNS answers from Go templates with regex matching, rcode, EDE codes and fallthrough, including the brace spacing pitfall."
sources:
  - https://coredns.io/plugins/template/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: answer queries dynamically without a backend.

Syntax:

```
template CLASS TYPE [ZONE...] {
    match REGEX...
    answer RR
    additional RR
    authority RR
    rcode CODE
    ederror EXTENDED_ERROR_CODE [EXTRA_REASON]
    fallthrough [FALLTHROUGH-ZONE...]
}
```

CLASS is usually IN or ANY; TYPE can be ANY. `match` defaults to `.*`, the first matching regex wins, and patterns must not exceed 10000 characters. Without `answer`, the response has an empty answer section. `rcode` defaults to NOERROR. `ederror` takes an RFC 8914 code (0 to 24).

Template data: `.Zone`, `.Name` (lowercased), `.Class`, `.Type`, `.Match`, `.Group` (named capture groups), `.Message`, `.Question`, `.Remote`, and `.Meta` (with the metadata plugin). Function: `parseInt`. Output must be an RFC 1035 style resource record.

Without fallthrough, if the zone matches but no regex does, the reply is SERVFAIL.

Pitfall: `{{$var}}` is read by CoreDNS as an environment variable reference; write `{{ $var }}` with spaces.

Example, mark .invalid as NXDOMAIN with a dummy SOA:

```
template ANY ANY invalid {
    rcode NXDOMAIN
    authority "invalid. 60 {{ .Class }} SOA ns.invalid. hostmaster.invalid. (1 60 60 60 60)"
    ederror 21 "Blocked according to RFC2606"
}
```

Metrics include `coredns_template_matches_total` and the two failure counters.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/template/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
