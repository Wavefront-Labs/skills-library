---
id: computing-software.web-development.frontend-development.locale-negotiation
name: locale-negotiation
category: computing-software
field: web-development
product: frontend-development
tags: [locale-negotiation, intl-locale, accept-language, navigator-languages, localized-routing, internationalization]
level: practitioner
status: docs-checked
description: "Choosing the user's locale: Accept-Language parsing, navigator.languages, BCP 47 matching with Intl.Locale and intl-localematcher, URL/cookie persistence and caching."
sources:
  - https://github.com/jshttp/negotiator#accept-language-negotiation
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Vary
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Language
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locale negotiation

## 1. Precedence
1. Explicit choice in the URL (`/fr/...`, `fr.example.com`) - shareable, crawlable.
2. Saved preference (cookie / user profile).
3. `Accept-Language` (server) or `navigator.languages` (client).
4. Default locale.
Do not pick language from geo-IP: a German speaker in Spain wants German.

## 2. Matching
```js
import Negotiator from "negotiator";
const negotiator = new Negotiator(req);          // req.headers carries Accept-Language
const requested = negotiator.languages();           // sorted by q-value
const locale = negotiator.language(["en-GB", "en-US", "fr", "de"]) ?? "en-GB";
```
In the browser, read `navigator.languages`, which generally lists the same locales as `Accept-Language`.
`Intl.Locale` parses and normalises tags:
```js
const l = new Intl.Locale("ja-JP-u-ca-gregory-hc-24");
l.baseName;                                  // "ja-JP"
new Intl.Locale("en").maximize().baseName;   // "en-Latn-US"
new Intl.Locale("fr-FR-u-hc-h23").hourCycle; // "h23"
```

## 3. Persist and route
- Redirect `/` -> `/fr/` only on first visit; keep a language switcher that sets a cookie and links to the same page in the other locale.
- `<html lang="fr">` per page.

## 4. Caching
If the response varies by `Accept-Language` or cookie without the locale in the URL, send `Vary: Accept-Language` so caches key on that header. Locale-in-URL avoids the problem.

## Gotchas
- Accept-Language may list only `en`; treat the region as optional.
- Separate **language** from **formatting region** and **currency**: a user may want English UI with euro prices and 24-hour time.
- Do not force-redirect clients away from the requested locale URL based on Accept-Language alone.

## Verify
- [ ] A request with `Accept-Language: fr-CA,fr;q=0.9,en;q=0.5` gets French; with a cookie set to `de`, German wins.

## Checked

2026-10-26. Negotiator README (languages() sorted by q-value, language(available)), MDN Intl.Locale (baseName, maximize, hourCycle and -u-hc extension), Vary and Accept-Language pages (Accept-Language generally mirrors navigator.languages). Removed the unconfirmed @formatjs matcher call, Chinese script advice, hreflang, framework helper and search-bot statements.

Method: documentation only; no commands were run.
