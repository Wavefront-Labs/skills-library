---
id: computing-software.cybersecurity-defensive.application-security.account-enumeration-prevention
name: account-enumeration-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [account-enumeration, username-enumeration, timing-attacks, generic-error-messages, authentication]
level: practitioner
status: docs-checked
description: "Prevent account enumeration on login, signup and reset: generic messages, equal-work timing, uniform HTTP status, and lockout and CAPTCHA choices per the OWASP cheat sheet."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Account enumeration prevention

Knowing which usernames or emails exist enables targeted credential stuffing, password spraying and phishing. The OWASP aim is to prevent a "discrepancy factor": login, password reset and recovery must respond generically, in both HTTP and HTML, whether the credentials are wrong, the account is missing, or it is locked or disabled.

## Leak channels and fixes
- **Messages.** Login: not "Login failed, invalid user ID" but "Login failed; Invalid user ID or password." Recovery: "If that email address is in our database, we will send you an email to reset your password." Registration: not "This user ID is already in use" but "A link to activate your account has been emailed to the address provided."
- **Status codes.** A generic page can still leak if the HTTP code differs (for example 200 for a valid account and 403 for an invalid one). Keep codes identical.
- **Timing.** A "quick exit" for a missing user makes failures faster than a wrong password for a real user. Do the same work in every case so that success and failure take comparable time.

Equal-work sketch (illustrative, not from the page; the cheat sheet describes the principle but does not name dummy hashes):
```python
DUMMY = ph.hash("dummy-password-for-timing")
def authenticate(username, password):
    user = find(username)
    try:
        ph.verify(user.pw_hash if user else DUMMY, password)
    except VerifyMismatchError:
        return None
    return user if user else None
```

## Lockout and automated attacks
- Tie the failed-login counter to the account, not the source IP.
- Lockouts can be abused to deny service to other users; one mitigation is to keep the forgotten-password flow working for locked accounts. Exponential lockout durations are an option.
- Throttle with a maximum number of attempts. CAPTCHA is a defence-in-depth control, not a preventative one; a friendly approach is to require it only after a small number of failed attempts.
- If the business accepts "already registered" messages for UX, document it and compensate with throttling on that endpoint (team practice, not stated by OWASP).

## Verify
Compare responses for an existing and a non-existing account on login, reset and signup: body, status, headers and timing should be indistinguishable.

## Checked
Method: 2026-11-08 read the Authentication Cheat Sheet's error-message, status-code, timing and automated-attack sections. The OWASP WSTG page cited earlier redirects to the guide home and its target page returns 404, so it was removed from sources. Dropped as unsupported: the claim of IP plus username throttling (the cheat sheet says to key on the account), the authenticated-lookup API rule, MFA-prompt and profile-URL channels, and the 50-request timing check. The dummy-hash code is a labelled illustration; the other leak-channel claims are unchanged.
