---
id: computing-software.software-engineering.clojure.routing-with-reitit-and-compojure
name: routing-with-reitit-and-compojure
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, routing, reitit, compojure, path-params, coercion, middleware, swagger, data-driven-routing, routing-reitit-compojure]
level: practitioner
status: draft
description: "Route requests with reitit (data-driven routes, path params, coercion, per-route middleware) or Compojure (defroutes, GET/POST macros) and choose between them."
sources: ["https://cljdoc.org/d/metosin/reitit/CURRENT", "https://github.com/weavejester/compojure"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Routing: reitit and Compojure

**Goal:** map URLs and methods to handlers.

## reitit (data-driven)
```clojure
(require '[reitit.ring :as ring])
(def app
  (ring/ring-handler
    (ring/router
      [["/ping" {:get (fn [_] {:status 200 :body "pong"})}]
       ["/users/:id" {:get {:handler (fn [{{:keys [id]} :path-params}] {:status 200 :body id})
                            :middleware [wrap-auth]}}]])
    (ring/create-default-handler)))      ; 404/405/406 responses
```
- Routes are plain vectors/maps, so they are inspectable, testable, and can generate docs (`reitit-swagger`).
- Coercion with malli or spec: `reitit.coercion.malli/coercion` plus `reitit.ring.coercion` middleware,
  declare `:parameters {:path [:map [:id int?]]}`.
- Route conflicts are detected at router creation.

## Compojure (macro-based)
```clojure
(require '[compojure.core :refer [defroutes GET POST context]])
(defroutes app-routes
  (GET "/users/:id" [id] (str "user " id))
  (POST "/users" {body :body} ...)
  (context "/api" [] (GET "/ping" [] "pong"))
  (compojure.route/not-found "Not found"))
```
- Compojure routes try in order and the first non-nil response wins; return nil to fall through.
- Path params are strings; convert/validate yourself (no coercion).

## Failure modes
- `405 Method Not Allowed` in reitit when the method key is missing.
- Ordering bugs: broad Compojure routes before specific ones.

## Self-check
Request an unknown path and a wrong method, verify 404 and 405 behaviour.
