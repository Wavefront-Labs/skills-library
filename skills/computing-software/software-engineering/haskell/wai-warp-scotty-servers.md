---
id: computing-software.software-engineering.haskell.wai-warp-scotty-servers
name: wai-warp-scotty-servers
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, wai, warp, scotty, yesod, http-server, middleware, routing, wai-middleware, wai-warp-scotty-servers, haskell-web]
level: practitioner
status: docs-checked
description: "Serve HTTP from Haskell with WAI and Warp, route with Scotty (captureParam, jsonData, middleware), and tune Warp settings: timeout, graceful shutdown, exceptions, TLS."
sources: ["https://hackage.haskell.org/package/scotty/docs/Web-Scotty.html", "https://hackage.haskell.org/package/warp/docs/Network-Wai-Handler-Warp.html", "https://hackage.haskell.org/package/warp-tls/docs/Network-Wai-Handler-WarpTLS.html", "https://hackage.haskell.org/package/wai", "https://hackage.haskell.org/package/wai-extra/docs/Network-Wai-Middleware-RequestLogger.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAI, Warp and Scotty

**Goal:** a small HTTP service. Packages: `wai`, `warp`, `scotty`, `aeson`.

```haskell
{-# LANGUAGE OverloadedStrings #-}
import Web.Scotty
import Data.Aeson (object, (.=))
import Network.Wai.Middleware.RequestLogger (logStdoutDev)

main :: IO ()
main = scotty 3000 $ do
  middleware logStdoutDev
  get "/hello/:name" $ do
    name <- captureParam "name"
    text ("hello " <> name)
  post "/items" $ do
    item <- jsonData :: ActionM Item       -- decodes request body with FromJSON
    json (object ["ok" .= True])
```
Raw WAI: `type Application = Request -> (Response -> IO ResponseReceived) -> IO ResponseReceived`; run with
`Network.Wai.Handler.Warp.run 8080 app` or `runSettings (setPort 8080 defaultSettings) app`. `setHost` takes a `HostPreference` (default `HostIPv4`).

## Production notes
- Warp settings: `setTimeout` (the slow-loris timeout, default 30 seconds), `setInstallShutdownHandler` with `setGracefulShutdownTimeout` (`Nothing` waits indefinitely, a number is seconds; graceful shutdown starts when the server socket is closed), `setOnException` (what to do with exceptions thrown by the application or the server), `setMaxTotalHeaderLength`.
- TLS: `warp-tls` provides `runTLS :: TLSSettings -> Settings -> Application -> IO ()`.
- Middleware (WAI): `wai-extra` has `Network.Wai.Middleware.RequestLogger` (`logStdoutDev`); `wai-cors` is a CORS middleware package; `wai-middleware-static` serves static files via `Network.Wai.Middleware.Static`.
- Servant covers typed APIs (see the servant skill).

## Gotchas
- Exceptions from the application reach `setOnException`; set it to log them.
- Use `Text` or `ByteString` for bodies rather than `String`.

## Self-check
- [ ] `curl localhost:3000/hello/x` returns the expected body.
- [ ] Graceful shutdown on SIGTERM verified.

## Checked
2026-11-03. Confirmed against the Haddock pages for `Web.Scotty` (`scotty`, `get`, `post`, `captureParam`, `jsonData`, `middleware`, `text`, `json`), `Network.Wai.Handler.Warp` (`run`, `runSettings`, `setPort`, `setHost`, `setTimeout`, `setInstallShutdownHandler`, `setGracefulShutdownTimeout`, `setOnException`, `setMaxTotalHeaderLength`), `WarpTLS` (`runTLS`), the `wai` `Application` type, `RequestLogger` (`logStdoutDev`) and the wai-cors and wai-middleware-static package pages. Removed: `-threaded`/`-with-rtsopts` advice, per-connection threads claim, other-framework list, wai-extra gzip claim, 500-response and bind-address advice.
Method: documentation only; no commands were run.
