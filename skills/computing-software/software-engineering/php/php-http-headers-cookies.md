---
id: computing-software.software-engineering.php.php-http-headers-cookies
name: php-http-headers-cookies
category: computing-software
field: software-engineering
product: php
tags: [php, http-headers-cookies, http]
level: practitioner
status: docs-checked
description: "Send headers and cookies from PHP with header(), http_response_code() and the setcookie() options array (SameSite, Secure, HttpOnly); avoid output before headers."
sources: ["https://www.php.net/manual/en/function.header.php", "https://www.php.net/manual/en/function.setcookie.php", "https://www.php.net/manual/en/function.header-remove.php", "https://www.php.net/manual/en/function.http-response-code.php", "https://www.php.net/manual/en/function.getallheaders.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP headers and cookies

```php
header('Content-Type: application/json; charset=utf-8');
header('X-Example: a');
header('X-Example: b', false);         // replace=false adds a second header of the same type
header_remove('X-Powered-By');         // expose_php is php.ini only

setcookie('prefs', $value, [           // options-array signature, PHP 7.3.0+
    'expires'  => time() + 86400,      // Unix timestamp
    'path'     => '/',
    'secure'   => true,
    'httponly' => true,
    'samesite' => 'Lax',               // None, Lax or Strict
]);
http_response_code(204);
header('Location: /next', true, 303); exit;
```
Read request headers with `getallheaders()`; its keys are not case-normalised, so lower-case them first (`array_change_key_case(getallheaders(), CASE_LOWER)`) because header names are case-insensitive.

## Gotchas
- `header()` must be called before any actual output, including blank lines or spaces in an included file; otherwise it fails. `headers_sent()` reports whether and where output began.
- `Location:` also sends a 302 status unless a 201 or 3xx code is already set; the third argument of `header()` sets the code (for example 301 or 303).
- Code after a redirect keeps running unless you `exit`.
- `setcookie()` options keys: `expires`, `path`, `domain`, `secure`, `httponly`, `samesite` (plus `partitioned`). If `samesite` is omitted no SameSite attribute is sent.
- `samesite` `None` requires `secure`, or the client blocks the cookie.
- The `secure` flag only asks the client to send the cookie over HTTPS; the manual says it is up to the programmer to send such a cookie only on a secure connection.
- `header_remove()` removes headers set by PHP such as `X-Powered-By`; `expose_php` can only be set in php.ini.

Verify: in a web SAPI, inspect the response headers (browser dev tools) for the status, `Location` and `Set-Cookie` attributes you expect.

## Checked
2026-11-03. Confirmed on the header, setcookie, header_remove, http_response_code and getallheaders manual pages. Removed (not confirmed in fetched text): CSP/HSTS/Cache-Control values, OWASP secure-header advice (page not read), `__Host-` prefix rules, header-injection and open-redirect remarks, session cookie ini advice, curl commands, `$_SERVER['HTTP_*']` reading.
Method: documentation only; no commands were run.
