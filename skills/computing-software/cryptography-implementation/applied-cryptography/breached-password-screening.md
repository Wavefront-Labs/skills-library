---
id: computing-software.cryptography-implementation.applied-cryptography.breached-password-screening
name: breached-password-screening
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, breached-password-check, password-blocklist, hibp, pwned-passwords, k-anonymity, sp-800-63b, password-policy]
level: practitioner
status: docs-checked
description: "Screen new passwords against breach corpora per NIST SP 800-63B: HIBP k-anonymity range API, local blocklists, padding, failure handling and UX."
sources: ["https://pages.nist.gov/800-63-4/sp800-63b.html", "https://haveibeenpwned.com/API/v3#PwnedPasswords", "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Breached password screening

NIST SP 800-63B requires verifiers to compare new passwords against a blocklist of commonly used, expected or
compromised values, and to drop composition rules and forced periodic changes.

## HIBP Pwned Passwords range API (k-anonymity)
```python
import hashlib, requests
def breach_count(pw: str) -> int:
    h = hashlib.sha1(pw.encode("utf-8")).hexdigest().upper()
    prefix, suffix = h[:5], h[5:]
    r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}",
                     headers={"Add-Padding": "true", "User-Agent": "example-app"}, timeout=3)
    r.raise_for_status()
    for line in r.text.splitlines():
        s, c = line.split(":")
        if s == suffix:
            return int(c)
    return 0
```
- Only the first 5 hex characters of the SHA-1 leave your server; `Add-Padding` hides the response size.
- SHA-1 here is a lookup key, not password storage.
- The API can also return NTLM hash suffixes instead of SHA-1; select this with the `mode` query string
  (see the HIBP API page).

## Offline option
For air-gapped or high-volume systems, load a downloaded corpus or a trimmed blocklist into a sorted file or similar
structure and refresh it periodically. NIST notes excessively large blocklists add little benefit against online
attacks.

## Policy
- Check at registration and password change (and optionally on login, prompting a change).
- Reject with a clear message ("This password has appeared in a data breach"), not a vague error.
- Combine with a context list: product name, username, email local part.
- Minimum length 15 for single-factor passwords (8 when used only within multi-factor authentication) under SP
  800-63B Rev 4; permit a maximum length of at least 64 and accept Unicode.

## Failure handling
If the API is down, fall back to a local blocklist rather than blocking signups; log and alert.

## Checked
2026-11-01. Confirmed in NIST SP 800-63-4 (63B): blocklist comparison on set/change, whole-password match,
context-specific words, no other composition rules, no periodic change, 15/8 minimum, 64 maximum, Unicode, reason for
rejection. Confirmed on the HIBP API page: range endpoint with first 5 SHA-1 characters, `Add-Padding`, NTLM via the
`mode` query string. Removed: the downloader tool name, the 100k list size, the "no key" claim, `?mode=ntlm` literal.
Method: documentation only; no commands were run.

## Verify
- [ ] "password123" is rejected; a fresh random passphrase is accepted.
- [ ] Network capture shows only 5-character prefixes sent.
- [ ] Timeout path uses the local list.
