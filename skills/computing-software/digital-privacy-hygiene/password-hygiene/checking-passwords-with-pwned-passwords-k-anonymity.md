---
id: computing-software.digital-privacy-hygiene.password-hygiene.checking-passwords-with-pwned-passwords-k-anonymity
name: checking-passwords-with-pwned-passwords-k-anonymity
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, pwned-passwords-api, have-i-been-pwned, k-anonymity, breached-password-check, password-blocklist, sha1-prefix, password-strength]
level: practitioner
status: draft
description: "Check whether a password appears in breach corpora without revealing it, using the Pwned Passwords k-anonymity range API, a password manager report, or the offline list."
sources:
  - "https://haveibeenpwned.com/API/v3#PwnedPasswords"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checking passwords against breach corpora

**Goal:** a password that appears in a breach list will be tried early by attackers,
however strong it looks. NIST requires verifiers to block such passwords; you can check
your own.

## How k-anonymity works
SHA-1 hash the password locally, send only the **first 5 hex characters** to
`https://api.pwnedpasswords.com/range/<prefix>`. The API returns all suffixes (hundreds)
with that prefix plus counts; you compare locally. The service never sees the full hash.

## Easiest: password manager reports
- Bitwarden: Reports > **Exposed passwords**.
- 1Password: Watchtower > Compromised passwords.
- KeePassXC: Reports > HIBP (online) or `keepassxc-cli analyze --hibp` (offline).
- Apple Passwords / Google Password Checkup: built in.

## Manual check (one password)
```bash
read -s -p "Password: " P; echo
H=$(printf '%s' "$P" | sha1sum | awk '{print toupper($1)}'); unset P
curl -s "https://api.pwnedpasswords.com/range/${H:0:5}" | grep -i "^${H:5}:" || echo "not found"
```
Add header `Add-Padding: true` to the request to hide response size.

## Interpreting results
- Found with any count: **retire it everywhere**, even if count is 1.
- Not found: doesn't mean strong; just not in known breaches.

## Gotchas
- Don't paste passwords into random "check my password" websites.
- Shell history: `read -s` avoids putting the password on the command line.

## Verify
- [ ] Manager's exposed-password report shows zero.
