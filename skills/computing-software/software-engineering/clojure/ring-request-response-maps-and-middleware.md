---
id: computing-software.software-engineering.clojure.ring-request-response-maps-and-middleware
name: ring-request-response-maps-and-middleware
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, ring, handler, middleware, request-map, response-map, jetty, http-kit, wrap-params, web, ring-handlers-middleware, clojure-web]
level: practitioner
status: draft
description: "Build web apps on Ring: handler functions over request/response maps, middleware composition order, running Jetty or http-kit, and common wrap-* middleware."
sources: ["https://github.com/ring-clojure/ring/wiki", "https://github.com/ring-clojure/ring"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ring handlers and middleware

**Goal:** understand the HTTP abstraction almost all Clojure web libraries share.

```clojure
(defn handler [request]
  {:status 200 :headers {"Content-Type" "text/plain"} :body "hello"})

(defn wrap-timing [h]
  (fn [req] (let [t (System/nanoTime) resp (h req)]
              (assoc-in resp [:headers "X-Time"] (str (- (System/nanoTime) t))))))

(require '[ring.adapter.jetty :refer [run-jetty]])
(defonce server (run-jetty #'app {:port 3000 :join? false}))   ; #' var keeps live reload working
(.stop server)
```
- Request map keys: `:request-method` (keyword), `:uri`, `:query-string`, `:headers` (lowercased string keys), `:body`
  (InputStream), `:remote-addr`, `:scheme`, `:server-port`.
- Middleware is `handler -> handler`; the LAST wrapper in `(-> handler a b c)` runs FIRST on the request.
- Common middleware: `wrap-params` (query/form params), `wrap-keyword-params`, `wrap-json-body` / `wrap-json-response`
  (ring-json), `wrap-resource`, `wrap-content-type`, `wrap-defaults` (ring-defaults bundle, including anti-forgery
  and secure headers for site-defaults).
- Async: Ring 1.6+ handlers may have 3 args `[req respond raise]`; adapters like Jetty support it.
- Pass the var (`#'app`) to `run-jetty` so redefinition at the REPL takes effect.
- Alternatives to Jetty: http-kit, Aleph, Immutant (check maintenance status).

## Failure modes
- Reading `:body` twice: the InputStream is consumed once; middleware may replace it with parsed data.
- Forgetting `:join? false` blocks the REPL.

## Self-check
`curl -i localhost:3000/` returns 200 with your header; add a middleware and see the extra header.
