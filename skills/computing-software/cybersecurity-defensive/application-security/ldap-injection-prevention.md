---
id: computing-software.cybersecurity-defensive.application-security.ldap-injection-prevention
name: ldap-injection-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [ldap-injection, injection, ldap-filter-escaping, active-directory, cwe-90, secure-coding]
level: practitioner
status: docs-checked
description: "Prevent LDAP injection: escape filter and DN values per RFC 4515 and RFC 4514, use library encoders or parameterized filters, and reject empty-password binds."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html", "https://datatracker.ietf.org/doc/html/rfc4515", "https://datatracker.ietf.org/doc/html/rfc4514", "https://cwe.mitre.org/data/definitions/90.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP injection prevention

Applications that build LDAP search filters or DNs from user input (login against AD/LDAP, directory search,
group lookups) are injectable if they concatenate strings. LDAP injection can grant unauthorised query results and
allow content modification inside the LDAP tree. It is common because LDAP has no widely used parameterized query
interface and is widely used to authenticate users.

## The bug
```java
String filter = "(&(uid=" + userInput + ")(objectClass=person))";
```
Untrusted input changes the filter logic, the same way as SQL injection.

## Primary defence 1: escape with the right encoder for the context
DNs and search filters have different escaping rules (RFC 4514 and RFC 4515). Avoid custom escaping code; use a
library encoder for the correct context.
- **Search filter values (RFC 4515)**: escape `*`, `(`, `)`, `\` and NUL as a backslash plus two hex digits, for
  example `\2a`, `\28`, `\29`, `\5c`, `\00`. Octets above 0x7F that are not part of valid UTF-8 are not allowed.
- **DN values (RFC 4514)**: escape a leading space or `#`, a trailing space, and the characters `"`, `+`, `,`, `;`,
  `<`, `=`, `>` and `\` (backslash prefix or `\XX` hex form).
- OWASP ESAPI: `encodeForLDAP(String)` for filter values, `encodeForDN(String)` for DN values.
- .NET: the AntiXSS `Encoder` class has `LdapFilterEncode` and `LdapDistinguishedNameEncode`; the cheat sheet also
  recommends LINQ to LDAP, which encodes automatically.
- Java JNDI: pass values as parameters to the search call, for example the filter `(&(uid={0})(objectClass=person))`
  with the user value in the `Object[]` argument of `ctx.search`, instead of concatenating.

## Primary defence 2: use a framework that escapes automatically

## Bind safely
- Reject empty passwords before binding: a non-empty name with an empty password can perform an unauthenticated
  bind that establishes anonymous authorisation, and a successful result does not prove identity.
- Authenticated binds do not stop user input altering a search filter; keep escaping even with valid credentials.
- Use a least-privileged binding account.

## Also
- Allowlist input validation as defence in depth (see the Input Validation cheat sheet). If special characters must
  be allowed, normalise input before validation.
- Code review: check every untrusted input fed into LDAP queries is escaped correctly. OWASP ZAP has modules that
  detect LDAP injection.

## Checked
Method: docs-checked 2026-11-09 against the OWASP LDAP Injection Prevention Cheat Sheet (read in full), RFC 4515
(escape examples and UTF-8 rules) and RFC 4514 (DN escaping section). Removed unconfirmed claims: library-specific
helpers for Spring LDAP, ldap3, python-ldap and PHP, the example injection string, the RFC 4513 reference and the
TLS and StartTLS advice.
