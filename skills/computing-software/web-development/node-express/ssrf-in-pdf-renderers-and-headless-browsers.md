---
id: computing-software.web-development.node-express.ssrf-in-pdf-renderers-and-headless-browsers
name: ssrf-in-pdf-renderers-and-headless-browsers
category: computing-software
field: web-development
product: node-express
tags: [html-to-pdf-ssrf, puppeteer-security, wkhtmltopdf, imagemagick-policy, ssrf, security]
level: advanced
status: docs-checked
description: "Stopping SSRF and local file reads through HTML-to-PDF renderers, headless Chrome screenshots, ImageMagick, ffmpeg and SVG rasterisers that fetch attacker-controlled URLs."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
  - https://pptr.dev/guides/network-interception
  - https://github.com/ImageMagick/ImageMagick/tree/main/config
  - https://ffmpeg.org/ffmpeg-protocols.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSRF in renderers and headless browsers

Rendering user HTML/Markdown into PDFs or screenshots gives the attacker a browser inside your network:
```html
<iframe src="http://169.254.169.254/latest/meta-data/iam/security-credentials/"></iframe>
<img src="file:///etc/passwd"><link rel="stylesheet" href="http://10.0.0.5:6379/">
```

## 1. Puppeteer / Playwright
```js
await page.setJavaScriptEnabled(false);                 // if the template does not need JS
await page.setRequestInterception(true);
page.on("request", req => {
  const u = new URL(req.url());
  if (u.protocol === "data:" || (u.protocol === "https:" && ALLOWED_HOSTS.has(u.hostname))) req.continue();
  else req.abort();
});
await page.setContent(html, { waitUntil: "networkidle0", timeout: 15000 });
```
- Block `file:`, `http:` to internal ranges, and redirects to them; test that every redirect hop is checked (see `HTTPRequest.redirectChain()`).
- Prefer inlining assets (fonts/images as data URLs) so no network is needed at all.

## 2. Isolate the renderer
- Run it in a separate container/network with egress only via an allowlisting proxy; no cloud credentials; block the cloud metadata address from that network.
- No shared volumes with secrets; read-only filesystem; per-job timeouts and memory limits.
- Treat the output as untrusted too (PDF with injected links/JS).

## 3. Other renderers
- **wkhtmltopdf**: the upstream repository is archived. Local file access is off by default (`--disable-local-file-access`); `--enable-local-file-access` turns it on and `--allow <path>` permits specific folders, so never enable it for untrusted input. Prefer headless Chrome.
- **ImageMagick**: start from the shipped `policy-secure.xml` or `policy-websafe.xml` (resource limits, delegates disabled with `rights="none" pattern="*"`, path rules blocking `@*`, `|*` and `/etc/*`) and add coder restrictions for your format allowlist; or use libvips/sharp.
- **ffmpeg** on user media: restrict input protocols with `protocol_whitelist` (comma-separated; a `-` prefix disables a protocol), for example `-protocol_whitelist file,pipe`, and avoid processing playlists from users.
- **SVG rasterisers**: sanitise SVG or rasterise with network disabled.
- Office converters (LibreOffice headless): run sandboxed and offline.

## Verify
- [ ] Rendering a template containing metadata-IP iframe, `file://` image and an internal host link produces a PDF without that content, and the proxy logs show blocked requests.

## Checked

2026-10-25 against the Puppeteer docs (puppeteer/puppeteer main), wkhtmltopdf usage text (archived repository), FFmpeg protocols doc, ImageMagick shipped policy files and the OWASP SSRF cheat sheet. Confirmed: Puppeteer request interception requires every request to be continued, responded or aborted; setJavaScriptEnabled, setContent waitUntil and HTTPRequest.redirectChain exist; wkhtmltopdf upstream is archived (last push 2022-11-22) and --disable-local-file-access is the default, with --enable-local-file-access and --allow <path>; FFmpeg protocol_whitelist is a comma-separated list where a - prefix disables a protocol; ImageMagick policy-secure.xml and policy-websafe.xml (resource limits, delegate and path rules) contain no coder entries.

Method: documentation only; no commands were run.
