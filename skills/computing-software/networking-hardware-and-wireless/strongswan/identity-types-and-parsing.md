---
id: computing-software.networking-hardware-and-wireless.strongswan.identity-types-and-parsing
name: identity-types-and-parsing
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, identities, identity-parsing, fqdn, distinguished-name, key-id]
level: advanced
status: docs-checked
description: "How strongSwan parses identity strings in swanctl.conf into DN, FQDN, RFC822, IP and KEY_ID types, the @ prefixes, explicit type prefixes and the %any wildcard."
sources:
  - https://docs.strongswan.org/docs/latest/config/identityParsing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# identity types and parsing
Identity strings (e.g. `local.id`, `eap` secret `id`) are typed by these rules, in order:

1. Contains `=`: a Distinguished Name, RDNs separated by commas, or by slashes if the string starts with `/`. If ASN.1 encoding fails, the type is KEY_ID with the literal string.
2. Contains `@`:
   - starts `@#`: KEY_ID from hex (quote it, since `#` starts a comment)
   - starts `@@`: USER_FQDN/RFC822 with the text after the prefix
   - starts `@`: FQDN with the text after the prefix (current versions do not resolve FQDNs when parsing identities)
   - otherwise: USER_FQDN/RFC822
3. No `@` or `=`:
   - empty, `%any`, `%any6`, `0.0.0.0`, `::` or `*`: ID_ANY, matching any identity
   - contains `:`: IPv6 address (CIDR subnets and `a-b` ranges are parsed too, usable only to match remote identities or define secrets); failing that KEY_ID
   - otherwise an IPv4 address, subnet or range, and failing that FQDN (domain names and simple names)

**Explicit type:** `<type>:<value>` with types `ipv4 ipv6 ipv4net ipv6net ipv4range ipv6range rfc822 email userfqdn fqdn dns asn1dn asn1gn keyid`, or a custom numeric type in curly brackets. A value starting with `#` is hex; otherwise the string is used as-is. No conversion happens for non-string identities, so `ipv4:10.0.0.1` is not a valid ID_IPV4_ADDR; use `ipv4:#0a000001` or just rely on automatic conversion. `pki --dn` helps with ASN.1 subject DNs.

A value starting with `^` and ending with `$` is an extended POSIX regular expression (the page says since 6.0.2), e.g. `fqdn:^vpn[0-9]+\.strongswan\.org$`. Regular expressions only match remote identities.

## Checked
2026-11-04. Confirmed against the Identity Parsing page: parsing order, prefixes, ID_ANY values, IP forms, explicit types and the regular expression rule.

Method: documentation only; no commands were run.
