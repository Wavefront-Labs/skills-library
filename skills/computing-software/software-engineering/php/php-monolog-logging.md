---
id: computing-software.software-engineering.php.php-monolog-logging
name: php-monolog-logging
category: computing-software
field: software-engineering
product: php
tags: [php, monolog-logging, logging]
level: practitioner
status: docs-checked
description: "Set up PSR-3 logging with Monolog: handler stack, processors, JSON formatting, fingers-crossed buffering, context and resets."
sources: ["https://www.php-fig.org/psr/psr-3/", "https://github.com/Seldaek/monolog/blob/main/doc/01-usage.md", "https://github.com/Seldaek/monolog/blob/main/doc/02-handlers-formatters-processors.md", "https://github.com/Seldaek/monolog/blob/main/doc/03-utilities.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging with Monolog

```php
use Monolog\{Logger, Level};
use Monolog\Handler\StreamHandler;
use Monolog\Formatter\JsonFormatter;
use Monolog\Processor\{UidProcessor, PsrLogMessageProcessor};

$stream = new StreamHandler('php://stderr', Level::Info);
$stream->setFormatter(new JsonFormatter());
$log = new Logger('app');            // the argument is the channel name
$log->pushHandler($stream);
$log->pushProcessor(new PsrLogMessageProcessor());   // replaces {foo} with $context['foo']
$log->pushProcessor(new UidProcessor());             // adds a unique id to each record

$log->info('Order {id} paid', ['id' => $order->id, 'amount_cents' => 4200]);
$log->error('Payment failed', ['exception' => $e]);  // PSR-3: exceptions go under 'exception'
```
Application code should depend on `Psr\Log\LoggerInterface`, not Monolog.

## How it works
- A `Logger` has a channel and a handler stack. A record travels from the top: `pushHandler()` puts a handler on top, so the last one pushed runs first. Constructor/`setHandlers()` order is call order instead.
- Handlers take `$bubble` (default `true`); `false` stops the record reaching handlers below.
- Only the eight RFC 5424 levels exist (DEBUG 100, INFO 200, NOTICE 250, WARNING 300, ERROR 400, CRITICAL 500, ALERT 550, EMERGENCY 600). Custom levels are not available; add processors for tags or other data.
- A processor is any callable that receives the record and returns it, usually changing `extra`. Processors can also be pushed on a single handler.
- Each handler has a formatter (a default is created). `JsonFormatter` encodes records as JSON; `LineFormatter` takes an output template with `%datetime%`, `%channel%`, `%level_name%`, `%message%`, `%context%`, `%extra%`.
- `$logger->withName('security')` clones a logger with another channel.
- `FingersCrossedHandler` wraps another handler, accumulates all-level records until one reaches the chosen severity, then delivers everything including debug and info. `ErrorLevelActivationStrategy` and `ChannelLevelActivationStrategy` define the trigger.
- `WhatFailureGroupHandler` ignores exceptions from its child handlers, so a dead remote connection does not take the app down. `RotatingFileHandler` writes one file per day.
- `Monolog\ErrorHandler::register($logger)` routes PHP errors and exceptions into the logger; `->captureStackTraces()` records where warnings and notices came from (your formatter must print them, for example `LineFormatter::includeStacktraces()`).

## Gotchas
- In containers write to stderr or stdout and let the platform ship logs.
- Use placeholders and context, not string interpolation, so fields stay searchable and filterable.
- Never log passwords, tokens or card data; add a processor to redact known keys.
- Context holds arbitrary data; pass identifiers, not huge objects.
- Long-running workers: buffered handlers such as `FingersCrossedHandler` and `BufferHandler` grow memory, so call `$logger->reset()` between jobs (flushes buffers and resets state).

Verify: log several debug lines then an error through a fingers-crossed setup and confirm the buffered lines appear only then.

## Checked

Date: 2026-11-08. Read in full: PSR-3, Monolog 01-usage and 03-utilities. From 02-handlers-formatters-processors read the wrapper handlers section and the entries for RotatingFileHandler, JsonFormatter, PsrLogMessageProcessor and UidProcessor (not the whole page). Removed: Monolog 2 versus 3 `Level` enum statement, the `FingersCrossedHandler` constructor arguments and buffer size, the claim about what the JSON formatter prints for exceptions, and the jq verification.

Method: documentation only; no commands were run.
