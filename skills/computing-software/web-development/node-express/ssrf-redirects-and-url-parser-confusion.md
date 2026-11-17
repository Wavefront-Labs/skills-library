---
id: computing-software.web-development.node-express.ssrf-redirects-and-url-parser-confusion
name: ssrf-redirects-and-url-parser-confusion
category: computing-software
field: web-development
product: node-express
tags: [ssrf, server-side-request-forgery, url-parser-confusion, redirect-following, whatwg-url, url-validation, scheme-allowlist]
level: practitioner
status: verified
description: "Closing SSRF bypasses from redirects and URL-parser differentials: one WHATWG parser, scheme allowlists, manual redirect handling and userinfo tricks."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
  - https://url.spec.whatwg.org/
  - https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSRF: redirects and URL-parser confusion

**Goal:** the URL you validate is exactly the URL that gets fetched - no redirects or parser differences in between.

## 1. Parser differentials
Validation code and the HTTP client may parse the same string differently:
- `http://allowed.com@evil.com/` - userinfo; host is `evil.com` (checked with `new URL`; `username` is `allowed.com`).
- Numeric hosts are normalised by `new URL`: `0x7f000001`, `2130706433`, `127.1`, `017700000001` and full-width digits all give hostname `127.0.0.1`; `[::ffff:127.0.0.1]` becomes `[::ffff:7f00:1]` (brackets kept, so unwrap before range checks).
- `http://evil.com#@allowed.com`, `http://evil.com\@allowed.com` - fragment/backslash handling differs between libraries.
- `http://allowed.com.evil.com`, `http://allowed.com%2eevil.com`.
- Mixed case / trailing dot hosts (`ALLOWED.com.`).
- Non-HTTP schemes: `file:`, `gopher:` (classic for hitting Redis/SMTP), `dict:`, `ftp:`, `data:`.

**Rules:** parse once with the WHATWG `URL` class, validate the parsed object, then pass **the parsed object's serialisation** (`url.href`) to the client - never the raw input. Reject URLs with `username`/`password`. Allow only `https:` (and `http:` if truly needed).

## 2. Redirects
```js
async function safeFetch(raw, hops = 0) {
  if (hops > 3) throw new Error('too many redirects');
  const url = new URL(raw);
  await assertAllowed(url);                         // scheme, host, resolved IP (see allowlisting skill)
  const res = await fetch(url.href, { redirect: 'manual', signal: AbortSignal.timeout(5000) });
  if (res.status >= 300 && res.status < 400 && res.headers.get('location'))
    return safeFetch(new URL(res.headers.get('location'), url).href, hops + 1);
  return res;
}
```
In Node's fetch (undici) `redirect: 'manual'` returns the 3xx with its `Location` header (checked on Node 20: status 302, `type` basic, Location readable; a followed redirect to `file:` fails with `URL scheme must be a HTTP(S) scheme`, and `fetch('file:...')` and `gopher:` are rejected). Re-validate every hop - including scheme changes (`https` -> `http`, `http` -> `file` won't be followed by fetch, but other clients like curl/libcurl-based tools may).

## 3. Headless browsers and converters
HTML-to-PDF, image converters (ImageMagick, ffmpeg), SVG renderers and XML parsers (XXE) fetch URLs embedded in **content**. Run them with network disabled or through the egress proxy; disable external entity resolution in XML parsers.

## Verify
- [ ] Unit tests with the bypass strings above return "blocked".
- [ ] Redirect chain public -> private blocked at the hop.
- [ ] PDF renderer cannot load `http://169.254.169.254` from an `<img>` in user HTML.

## Checked
Run on Windows with Node 20.20.2: 25 inputs through `new URL` (userinfo, fragment and backslash tricks, `%2e`, trailing dot, numeric and IPv4-mapped hosts, `file:`, `gopher:`; `//evil.com` throws `ERR_INVALID_URL`); a local server redirecting to a loopback URL and to `file:`; `redirect: 'manual'` behaviour as above. `http://evil.com\@allowed.com` parses with host `evil.com` (backslash treated as slash). Linux pass: WHATWG URL parsing is built into Node and gave the same results on Linux (Node 20.20.2 musl in a WSL2 distro). Not run: curl or libcurl-based tools following redirects, ImageMagick, ffmpeg, headless browsers and PDF renderers (section 3 and the last Verify item are advice only).
