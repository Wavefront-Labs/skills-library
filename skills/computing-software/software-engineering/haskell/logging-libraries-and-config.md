---
id: computing-software.software-engineering.haskell.logging-libraries-and-config
name: logging-libraries-and-config
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, logging, katip, monad-logger, co-log, fast-logger, configuration, yaml, dotenv, envy, environment, logging-libraries-and-config, haskell-logging]
level: practitioner
status: draft
description: "Add structured logging (katip, monad-logger, co-log, fast-logger) with levels and contexts, and load configuration from env vars, YAML and files with validation."
sources: ["https://hackage.haskell.org/package//katip", "https://hackage.haskell.org/package//co-log"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logging and configuration

**Goal:** observable services with typed configuration.

## Logging options
- `monad-logger`: `MonadLogger` class with `logInfoN`, `logErrorN`, `runStdoutLoggingT`; used by persistent/yesod; simple, text-based. `fast-logger` underneath provides buffered, thread-safe output.
- `katip`: structured JSON/scribe-based logging with namespaces, severity and contextual payloads; supports multiple sinks.
- `co-log`: composable `LogAction m msg`, contravariant style.
- Plain approach: `hPutStrLn stderr` guarded by an `MVar`, or a logging function stored in the application `Env` (ReaderT pattern).
```haskell
data Env = Env { logInfo :: Text -> IO (), cfg :: Config }
-- tests pass `\_ -> pure ()` or a collector
```

## Configuration
```haskell
import System.Environment (lookupEnv)
import Data.Yaml (decodeFileEither)       -- package yaml
port <- maybe 8080 read <$> lookupEnv "PORT"   -- use readMaybe in real code
cfg  <- either (error . show) id <$> decodeFileEither "config.yaml"
```
Libraries: `envy`, `envparse` (typed env parsing), `dotenv`, `configurator`, `yaml` (FromJSON via aeson), `optparse-applicative` for flags. Layer: defaults, file, environment, flags; validate and fail fast at startup with all errors reported together.

## Practices
- Log at boundaries (requests, jobs), include request ids, avoid logging secrets (redacting `Show` newtypes).
- Flush on exit: `bracket` the logger close.
- Use levels consistently; make level configurable.
- Log failures with enough context, not stack dumps of lazy thunks.

## Gotchas
- Unbounded logging queues may exhaust memory under load; use bounded buffers.
- Lazy `show` inside log messages is evaluated even when the level filters it unless the API takes a lazy message.
- Interleaved output from threads without a lock.

## Self-check
- [ ] Config errors list all missing variables at once.
- [ ] No secret appears in logs under `DEBUG`.
