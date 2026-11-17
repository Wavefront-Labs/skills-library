---
id: computing-software.software-engineering.php.php-phpunit
name: php-phpunit
category: computing-software
field: software-engineering
product: php
tags: [php, php-testing-analysis, phpunit]
level: intro
status: draft
description: "Write PHPUnit tests with attributes, data providers and exception assertions."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PHPUnit tests and data providers
- `final class FooTest extends TestCase { public function testX(): void { $this->assertSame(3, add(1,2)); } }`; run `vendor/bin/phpunit`.
- Data providers: `#[DataProvider('cases')]` static method (PHPUnit 10+ attributes replace annotations); `expectException(Foo::class)` before the call.
- `phpunit.xml` config: bootstrap `vendor/autoload.php`, `failOnWarning`, `failOnRisky`.
- Prefer `assertSame` over `assertEquals` (loose).
Verify: `--coverage-text` with Xdebug or PCOV.
