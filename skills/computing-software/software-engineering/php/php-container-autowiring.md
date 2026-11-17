---
id: computing-software.software-engineering.php.php-container-autowiring
name: php-container-autowiring
category: computing-software
field: software-engineering
product: php
tags: [php, container-autowiring, dependency-injection]
level: practitioner
status: draft
description: "Wire PHP services with a PSR-11 container: autowiring, interface bindings, shared services, compiled containers and service-locator avoidance."
sources: ["https://www.php-fig.org/psr/psr-11/", "https://symfony.com/doc/current/service_container.html", "https://php-di.org/doc/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency injection containers and autowiring

A PSR-11 container exposes `get(string $id)` and `has(string $id)`, throwing `NotFoundExceptionInterface` / `ContainerExceptionInterface`.

```php
// PHP-DI (illustrative): autowires by constructor type-hints; bind interfaces explicitly
$builder = new DI\ContainerBuilder();
$builder->addDefinitions([
    LoggerInterface::class => DI\autowire(Monolog\Logger::class)->constructorParameter('name', 'app'),
    Mailer::class          => DI\create(SmtpMailer::class)->constructor(DI\env('SMTP_DSN')),
]);
$builder->enableCompilation(__DIR__ . '/var/cache');   // production
$container = $builder->build();

final class Checkout {
    public function __construct(private OrderRepository $orders, private LoggerInterface $log) {}  // autowired
}
```
Symfony equivalent: `config/services.yaml` with `_defaults: {autowire: true, autoconfigure: true}`, `App\: {resource: '../src/'}`, alias interface to implementation, tags for collections, `bin/console debug:container`.

## Practice
- Inject collaborators via the constructor; type-hint interfaces you own.
- Services are shared (one instance) by default; request-specific state belongs in per-request objects, not services, particularly in long-running workers.
- Compile or cache the container for production.
- Composition root only: wire the container in the entrypoint.

## Gotchas
- Passing the container into classes (service locator) hides dependencies and makes tests brittle; inject what you need.
- Autowiring cannot choose between several implementations of an interface; add an alias or a named binding.
- Scalar parameters (DSNs, keys) need explicit config; never autowire them.
- Circular dependencies mean a design problem; break with an event or a smaller service rather than lazy proxies.
- Behaviour differs by library (PHP-DI vs Symfony vs Laravel); check the docs for your version.

Verify: boot the container in a smoke test that resolves every public service (`debug:container --errors` in Symfony) to catch missing bindings in CI.
