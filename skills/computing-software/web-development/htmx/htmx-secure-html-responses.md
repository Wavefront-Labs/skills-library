---
id: computing-software.web-development.htmx.htmx-secure-html-responses
name: htmx-secure-html-responses
category: computing-software
field: web-development
product: htmx
tags: [htmx, security, xss, csrf, cookies, escaping, csp, samesite]
level: practitioner
status: docs-checked
description: "Four security rules for htmx apps: only call your own routes, auto-escape templates, put user content only inside HTML tags, and set auth cookies Secure, HttpOnly, SameSite=Lax."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/essays/web-security-basics-with-htmx.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid XSS and CSRF in an app whose server returns HTML that htmx inserts into the page.

Rule 1: only call routes you control. htmx inserts the response into the page, so a malicious `<script>` in a foreign response can steal user data. Use relative URLs: `<button hx-get="/events">` is fine, `hx-get="https://google.com/search?q=events"` is not. Serve the HTML frontend from the same server or domain as the backend (also avoids CORS). htmx 2 disables calling other domains by default.

Rule 2: always use an auto-escaping template engine. All dynamic content must be escaped, which blocks stored XSS such as a bio containing a script that posts `document.cookie` elsewhere. Defaults the essay lists: Nunjucks yes; EJS yes with `<%= %>`; Django templates yes; Jinja sometimes (yes in Flask); ERB yes with `<%= %>`; Blade yes; Go html/template yes; Thymeleaf yes; Tera yes. Escaping replaces `& < > " ' / `` ` `` =` with entities (for example `<` becomes `&lt;`).

Rule 3: user-generated content only inside HTML tags. Never in `<script>`, `<style>`, as a tag name, or as an attribute name:

```html
<a>{{ user.name }}</a>              <!-- fine -->
<a class="{{ user.class }}"></a>    <!-- attribute VALUES: sometimes okay, depends -->
<script>const userName = {{ user.name }}</script>   <!-- do not -->
<a {{ user.attribute }}></a>        <!-- do not -->
```
For links or images, let users supply a choice and generate the URL yourself (for example upload to your own storage and emit that URL unescaped, e.g. Nunjucks `| safe`). For CSS, map limited choices (red or blue) rather than accepting raw values. Arbitrary user URLs need a custom escaper that keeps `/`, and image links let third parties track users.

Rule 4: cookies. Authenticate with cookies and send:

```
Set-Cookie: token=asd8234nsdfp982; Secure; HttpOnly; SameSite=Lax
```
- `Secure`: HTTPS only. `HttpOnly`: not readable via `document.cookie`, so an injected script cannot steal it. `SameSite=Lax`: cross-site requests do not carry the cookie except for plain link navigation, blocking most CSRF (in 2024 usually enough; see OWASP for extra mitigations).
- `SameSite=Lax` works per registrable domain, not subdomains such as `yoursite.github.io`; do login on your own domain.
- Avoid an `Authorization` header with a token in local storage: there is no way to set it without JavaScript, and a token available to your JavaScript is available to attackers who get a malicious script onto the page.

Breaking rule 1: never call untrusted HTML APIs. For a third-party JSON API use `fetch` and `JSON.parse()`, then set `textContent`, not HTML, since JSON values can contain markup.

CSP: Content-Security-Policy is a worthwhile extra but has no one-size setting; `hx-on` evaluates inline scripts and can be disabled if unused.

## Checked

2026-11-07. Confirmed against the htmx essay "Web Security Basics (with htmx)" (the four golden rules, template-engine table, escaped character set, dangerous contexts, cookie attributes and `SameSite=Lax` domain caveat, untrusted-API and `Authorization` header sections, CSP and `hx-on` note). Reworded the `Authorization` bullet to the essay's wording and removed the invented Verify step. The essay is dated 2024-02, so engine defaults and the "in 2024" CSRF note reflect that date.
Method: documentation only; no commands were run.
