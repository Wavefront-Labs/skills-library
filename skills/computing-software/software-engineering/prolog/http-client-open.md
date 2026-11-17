---
id: computing-software.software-engineering.prolog.http-client-open
name: http-client-open
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, http-client-open, load-html]
level: practitioner
status: draft
description: "Fetch URLs with http_open/3, http_get/3 and parse results with library(http/json) or sgml load_html/3."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP client
```prolog
:- use_module(library(http/http_open)).
:- use_module(library(http/json)).
:- use_module(library(sgml)).
?- http_open('https://example.org/', S, []), read_string(S, _, Txt), close(S).
?- setup_call_cleanup(http_open('https://example.org/api', S, [request_header('Accept'='application/json')]),
                      json_read_dict(S, D), close(S)).
?- load_html(stream(S), DOM, []), xpath(DOM, //title(text), T).
```
- `library(xpath)` navigates parsed DOM.
## Gotchas
- Always close the stream (setup_call_cleanup).
- HTTPS needs the ssl package; set timeouts with `timeout(Seconds)` option.
- Respect robots.txt and rate limits when scraping.
## Self-check
Fetch a page and extract its title.
