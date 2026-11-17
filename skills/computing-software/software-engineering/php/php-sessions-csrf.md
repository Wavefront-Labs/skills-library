---
id: computing-software.software-engineering.php.php-sessions-csrf
name: php-sessions-csrf
category: computing-software
field: software-engineering
product: php
tags: [php, php-security, sessions-csrf]
level: advanced
status: docs-checked
description: "Harden PHP sessions: cookie flags, ID regeneration, and CSRF tokens."
sources: ["https://www.php.net/manual/en/function.session-set-cookie-params.php", "https://www.php.net/manual/en/function.session-regenerate-id.php", "https://www.php.net/manual/en/session.configuration.php", "https://www.php.net/manual/en/function.hash-equals.php", "https://www.php.net/manual/en/function.random-bytes.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sessions cookies and CSRF
- Cookie flags: `session_set_cookie_params(['secure' => true, 'httponly' => true, 'samesite' => 'Lax'])` (array signature since PHP 7.3). The manual says `samesite` must be `Lax` or `Strict`, and if it is omitted no SameSite attribute is set. The effect lasts only for the script, so call it on every request and before `session_start()`.
- `session.use_strict_mode` defaults to 0. When enabled, the module does not accept uninitialized session IDs and sends a new one, which protects against session fixation via session adoption.
- `session_regenerate_id()` on login and privilege change. Its `$delete_old_session` parameter defaults to false; the manual warns that deleting the old session immediately can cause races with concurrent requests and disables session hijack detection, so prefer keeping it briefly with a destroy timestamp (see the manual's examples).
- CSRF token: generate it with `random_bytes()` (the manual states it is suitable for all applications including long-term secrets), store it in the session, and compare the submitted value with `hash_equals($known, $user)`. The manual says to pass the secret known string first and the user-supplied string second. `hash_equals` avoids leaking contents through timing, unlike `===`.
- SameSite reduces cross-site cookie sending, but keep the token check as well.

Verify: inspect the Set-Cookie attributes in browser devtools; replay a request with a missing and a wrong token.

## Checked
2026-11-09. Confirmed against php.net manual pages session_set_cookie_params, session_regenerate_id, session configuration (session.use_strict_mode), hash_equals and random_bytes. Removed: claim that rand/mt_rand are unsuitable and the bin2hex encoding example (not stated on those pages); replaced landing-page sources with the specific pages. Read in full: set_cookie_params and hash_equals; others read for the cited passages.
Method: documentation only; no commands were run.
