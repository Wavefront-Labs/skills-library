---
id: computing-software.software-engineering.scheme-racket.web-server-servlets
name: web-server-servlets
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, web-server-servlets, racket-web-gui]
level: advanced
status: docs-checked
description: "Serve HTTP from Racket with serve/servlet (web-server/servlet-env) or #lang web-server/insta, a start function and response/xexpr; local-only by default."
sources:
  - https://docs.racket-lang.org/web-server/run.html
  - https://docs.racket-lang.org/web-server/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# web-server servlets
**Goal:** minimal web app.
```racket
#lang racket
(require web-server/servlet web-server/servlet-env)
(define (start req)
  (response/xexpr '(html (head (title "Hello world!")) (body (p "Hey out there!")))))
(serve/servlet start #:port 8080)
```
- `#lang web-server/insta` is the quickest route: define `start` and press Run in DrRacket; a browser opens and the servlet is reachable only from the local machine. `no-web-browser` and `static-files-path` customise it. In `serve/servlet`, `start` is not a special name.
- `serve/servlet` options shown in the manual: `#:port`, `#:listen-ip #f` (accept connections from external machines), `#:servlet-path` (default URL is `http://localhost:8000/servlets/standalone.rkt`), `#:servlet-regexp #rx""` (capture top-level requests), `#:extra-files-paths`, `#:command-line? #t` (no browser, no banner).
- A stateful servlet module exports `interface-version` (`'v2`), `manager` and `start`; `start` takes the initial `request?` and returns `can-be-response?`.
- `web-server/servlet/web`: `send/back` sends a response and ends the servlet; `send/suspend` captures the continuation and gives `make-response` a URL (`k-url`) to put in a form `action`; submitting returns the request from `send/suspend`.
- Keep `#:listen-ip` at its local default during development. Check request parameters and build pages as x-expressions rather than concatenated strings. (Security guidance, not a manual quote.)
## Self-check
Run the example and visit `http://localhost:8080/servlets/standalone.rkt`.

## Checked
2026-11-08. Confirmed against the Web Server manual pages Running Web Servlets (insta, servlet-env examples and options) and Stateful Servlets (v2 exports, send/back, send/suspend). Removed: `#lang web-server` as the example language and the `#:servlet-path "/"` setting (not shown), the GUI manual source (unrelated), and the claim that xexpr escapes text (not on pages read).
Method: documentation only; no commands were run.
