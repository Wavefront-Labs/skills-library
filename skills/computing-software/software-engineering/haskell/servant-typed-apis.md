---
id: computing-software.software-engineering.haskell.servant-typed-apis
name: servant-typed-apis
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, servant, servant-server, servant-client, api-type, generic-routes, openapi, servant-swagger, handler, servant-typed-apis]
level: advanced
status: docs-checked
description: "Define HTTP APIs as types with Servant combinators, serve them with servant-server and Warp, derive clients with servant-client, use hoistServer and NamedRoutes."
sources: ["https://hackage.haskell.org/package/servant/docs/Servant-API.html", "https://hackage.haskell.org/package/servant-server/docs/Servant-Server.html", "https://hackage.haskell.org/package/servant-client/docs/Servant-Client.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Servant

**Goal:** one type describes the API; server, client and docs derive from it.

```haskell
{-# LANGUAGE DataKinds, TypeOperators, DeriveGeneric, DeriveAnyClass #-}
import Servant
import Network.Wai.Handler.Warp (run)

type API = "users" :> Get '[JSON] [User]
      :<|> "users" :> Capture "id" Int :> Get '[JSON] User
      :<|> "users" :> ReqBody '[JSON] NewUser :> PostCreated '[JSON] User
      :<|> "search" :> QueryParam "q" Text :> Get '[JSON] [User]

server :: Server API
server = listUsers :<|> getUser :<|> createUser :<|> search
  where
    getUser :: Int -> Handler User
    getUser i = maybe (throwError err404) pure (lookup i db)

main = run 8080 (serve (Proxy :: Proxy API) server)
```
Client: `client (Proxy :: Proxy API)` yields functions that `servant-client` runs with `runClientM`.

## Facts
- Combinators: `:>` path/parts, `:<|>` alternatives, `Capture`, `QueryParam`, `ReqBody`, `Header`, `Verb` (with `PostCreated` an alias for `Verb 'POST 201`), `Raw`, `BasicAuth`, `AuthProtect`.
- Content types are listed as `'[JSON, PlainText]`.
- `Handler` wraps `ExceptT ServerError IO` (field `runHandler'`); `throwError` with a `ServerError` such as `err404` or `err401` sets the response; use `hoistServer` to serve handlers written in another monad.
- `Servant.API.NamedRoutes` provides the records-of-routes style.

## Gotchas
- Handlers must be in exactly the order of the type (`:<|>` alternatives).
- `ServerError` has an `errBody` field; update it on an error value (`err401 { errBody = ... }`) to send a body.
- Keep the API type in a library module shared by client and server.

## Self-check
- [ ] A change to the API type fails to compile in server and client until updated.
- [ ] Error responses have deliberate status codes.

## Checked
2026-11-03. Confirmed against the Haddock pages for `Servant.API` (`:>`, `:<|>`, `Capture`, `QueryParam`, `ReqBody`, `Verb`, `PostCreated`, `Raw`, `BasicAuth`, `AuthProtect`, `NamedRoutes`), `Servant.Server` (`serve`, `Handler`, `ServerError`, `err404`, `err401`, `errBody`, `throwError`, `hoistServer`) and `Servant.Client` (`client`, `runClientM`). Removed: servant-openapi3 and servant-docs, the NamedRoutes version gate, and the compile-time advice.
Method: documentation only; no commands were run.
