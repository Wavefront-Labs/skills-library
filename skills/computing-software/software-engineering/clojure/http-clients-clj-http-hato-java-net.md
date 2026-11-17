---
id: computing-software.software-engineering.clojure.http-clients-clj-http-hato-java-net
name: http-clients-clj-http-hato-java-net
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, http-client, clj-http, hato, java-http-client, babashka-http-client, timeouts, retries, http, http-client-requests]
level: practitioner
status: docs-checked
description: "Call HTTP APIs from Clojure with hato (java.net.http), clj-http or the JDK HttpClient directly; set timeouts, parse JSON, handle non-2xx and retries safely."
sources: ["https://github.com/gnarroway/hato", "https://github.com/dakrone/clj-http"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP clients

**Goal:** make reliable outbound calls.

```clojure
(require '[hato.client :as hc])
(def client (hc/build-http-client {:connect-timeout 5000 :redirect-policy :normal}))
(hc/get "https://api.example.com/items" {:http-client client :as :json :timeout 10000
                                         :headers {"Accept" "application/json"}})
(hc/post url {:body (json/write-str m) :content-type :json :as :json})
;; clj-http: (clj-http.client/get url {:as :json :socket-timeout 10000 :connection-timeout 5000})
```
- hato wraps the JDK 11+ HttpClient (HTTP/2 preferred by default, async via `:async? true` returning a
  CompletableFuture); clj-http wraps Apache HttpComponents.
- Always set connect and request timeouts: hato's `:connect-timeout` and `:timeout` default to unlimited.
- Both throw on exceptional statuses by default (`:throw-exceptions? false` in hato, `:throw-exceptions false` in
  clj-http to return the response instead). In hato's async mode the raise function gets an ex-info whose `ex-data`
  holds the response map (so `:status`).
- `:as :json` needs the optional cheshire dependency in both libraries; hato's `:coerce` defaults to
  `:unexceptional` (error bodies are not coerced).
- Retries: only for idempotent requests, with backoff and a cap; do not retry POSTs without idempotency keys.
- Reuse one client instance for connection pooling; do not create one per request.
- Secrets in URLs or logs: redact `Authorization` headers.
- JSON request bodies: pass `:content-type :json` with `:form-params` (hato, needs cheshire) or encode the body
  yourself as a string.

## Failure modes
- Hanging calls with no timeout.
- Memory blowup reading huge bodies with the default string body; use `:as :stream`.

## Self-check
Point the client at a closed port and at a slow endpoint; confirm both fail within your timeouts.

## Checked
2026-11-08. Confirmed on the hato README (build-http-client options, request options incl. `:timeout`, `:connect-timeout`, `:redirect-policy :normal`, `:as`, `:coerce`, `:throw-exceptions?`, `:async?`, ex-data on async raise, JDK 11 requirement, form-params with `:content-type :json`) and the clj-http README (Apache HttpComponents, `:socket-timeout`, `:connection-timeout`, `:throw-exceptions false`, `:as :json`/`:stream`, cheshire dependency). Removed: the claim that clj-http has a longer feature list, the direct JDK HttpClient example. The retry bullet is general engineering advice, not a library claim.
Method: documentation only; no commands were run.
