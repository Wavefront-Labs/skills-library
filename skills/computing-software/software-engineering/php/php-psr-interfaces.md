---
id: computing-software.software-engineering.php.php-psr-interfaces
name: php-psr-interfaces
category: computing-software
field: software-engineering
product: php
tags: [php, php-standards, psr-interfaces]
level: advanced
status: docs-checked
description: "Code against PSR logger, container, HTTP message, handler, factory and client interfaces for portability."
sources: ["https://www.php-fig.org/psr/psr-3/", "https://www.php-fig.org/psr/psr-11/", "https://www.php-fig.org/psr/psr-15/", "https://www.php-fig.org/psr/psr-17/", "https://www.php-fig.org/psr/psr-18/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSR-3, PSR-7, PSR-11, PSR-15, PSR-17 and PSR-18 interfaces

Depend on the interface in your own code and wire the implementation in one composition root.

- PSR-3 `Psr\Log\LoggerInterface`: eight methods for the RFC 5424 levels (debug, info, notice, warning, error, critical, alert, emergency) plus `log($level, ...)`. Messages may hold `{placeholder}` names that map to keys in the context array. An exception passed in context MUST be under the key `exception`. Users should not pre-escape placeholder values.
- PSR-7 messages are immutable: methods such as `withHeader()` return a new instance, so keep the return value. Header names are case-insensitive. `getHeader()` returns an array; `getHeaderLine()` returns the values joined by commas, which is not safe for `Set-Cookie`, so use `getHeader()` there. A body is a `StreamInterface`, which (unlike messages) is not immutable.
- PSR-11 `Psr\Container\ContainerInterface` has `get` and `has`. `get` throws `NotFoundExceptionInterface` for an unknown id, and `has($id) === false` means `get($id)` must throw it. Do not pass the container into an object so it can fetch its own dependencies (service locator).
- PSR-15 `RequestHandlerInterface::handle()` and `MiddlewareInterface::process()`; the spec recommends one exception-catching middleware that runs first.
- PSR-17 factories (`RequestFactoryInterface`, `ResponseFactoryInterface`, ...) create PSR-7 objects without tying code to one implementation.
- PSR-18 `Psr\Http\Client\ClientInterface::sendRequest()`: a 4xx or 5xx response is returned normally and never raises an exception. Failure to send throws `ClientExceptionInterface`, with `RequestExceptionInterface` for a malformed request and `NetworkExceptionInterface` for network failure including timeout.
- PSR-6 and PSR-16 caching are covered in the php-psr-cache skill.

Verify: swap implementations in a test to prove no coupling.

## Checked

Date: 2026-11-08. Read in full from the php-fig/fig-standards markdown: PSR-3, PSR-11, PSR-15, PSR-18. Read the PSR-7 specification text (sections 1.1 to 1.5, about the first 330 lines) and searched the rest for immutability wording; PSR-17 was read to its first interface only (the opening and RequestFactory/ResponseFactory sections). Removed the unread php.net manual source and the unsourced PSR-6/16 detail (now in php-psr-cache).

Method: documentation only; no commands were run.
