---
id: computing-software.software-engineering.r.r-httr2-jsonlite
name: r-httr2-jsonlite
category: computing-software
field: software-engineering
product: r
tags: [r, r-web, httr2-jsonlite]
level: practitioner
status: draft
description: "Call REST APIs with httr2 including auth, retry and throttling, and parse JSON with jsonlite."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# httr2 requests, retries and jsonlite parsing
- `request(url) |> req_url_query(page = 1) |> req_auth_bearer_token(tok) |> req_retry(max_tries = 3) |> req_perform()`.
- `resp_body_json(resp)` and `resp_status(resp)`; httr2 errors on HTTP 4xx/5xx by default (`req_error()` customises).
- `req_throttle()` for rate limits.
- `jsonlite::fromJSON(txt, simplifyVector = TRUE)` and `toJSON(x, auto_unbox = TRUE)`; length-one vectors become arrays unless `auto_unbox` is set.
Verify: use `httr2::with_mocked_responses()` in tests.
