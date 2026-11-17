---
id: computing-software.software-engineering.php.php-psr15-middleware
name: php-psr15-middleware
category: computing-software
field: software-engineering
product: php
tags: [php, psr15-middleware, http]
level: practitioner
status: docs-checked
description: "Build PSR-15 middleware and request handlers on PSR-7/17 objects: ordering, short-circuiting, immutability and error handling."
sources: ["https://www.php-fig.org/psr/psr-15/", "https://www.php-fig.org/psr/psr-7/", "https://www.php-fig.org/psr/psr-17/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSR-15 middleware pipelines

```php
use Psr\Http\Message\{ServerRequestInterface, ResponseInterface, ResponseFactoryInterface};
use Psr\Http\Server\{MiddlewareInterface, RequestHandlerInterface};

final class RequireApiKey implements MiddlewareInterface {
    public function __construct(private ResponseFactoryInterface $rf, private array $keys) {}
    public function process(ServerRequestInterface $req, RequestHandlerInterface $next): ResponseInterface {
        $key = $req->getHeaderLine('X-Api-Key');
        foreach ($this->keys as $k) { if (hash_equals($k, $key)) { return $next->handle($req->withAttribute('client', $k)); } }
        return $this->rf->createResponse(401)->withHeader('WWW-Authenticate', 'ApiKey');   // short-circuit
    }
}
```

## What the specs say
- `MiddlewareInterface::process(ServerRequestInterface, RequestHandlerInterface): ResponseInterface`; `RequestHandlerInterface::handle(ServerRequestInterface): ResponseInterface`.
- A middleware MAY return a response without calling the handler (short-circuit). A request handler MAY throw if it cannot produce a response.
- Recommended: compose a response factory (PSR-17 `ResponseFactoryInterface::createResponse(int $code = 200, string $reasonPhrase = '')`) or a prototype response so code is not tied to one PSR-7 implementation.
- Recommended: one component that catches exceptions and turns them into responses; it SHOULD be the first component executed and wrap all further processing.
- PSR-7 messages are immutable: every `with*()` returns a new instance, so use the returned value (`$req = $req->withAttribute(...)`). Request attributes are the channel between consumers.
- Header names are case-insensitive. `getHeader()` returns an array of values; `getHeaderLine()` joins them with commas (not suitable for `Set-Cookie`).
- Bodies are `StreamInterface` objects, which are not immutable and may be non-seekable; check `isSeekable()` before re-reading and avoid casting huge bodies to string.

## Practice (judgement, not in the specs)
- Keep middleware single-purpose and pass data via attributes.
- Order is a security decision: put authentication before anything that trusts the identity, and write a test per route class.
- Post-processing happens on the way back out, on the response returned by `$next->handle()`.
- Forgetting to call `$next->handle()` drops the rest of the stack; only do it deliberately.

Verify: unit test each middleware with a fake handler, then an integration test of a protected route with and without the key.

## Checked

Date: 2026-11-08. Read in full: PSR-15; PSR-7 sections 1.1 to 1.5 (headers, streams, immutability notes; first 330 lines plus a search of the rest for immutability); PSR-17 opening and ResponseFactoryInterface. Removed the named PSR-7 implementations (Nyholm, Guzzle, Laminas), because no cited page lists them, and the claim that `rewind()` is needed (the specs only say streams may be non-seekable).

Method: documentation only; no commands were run.
