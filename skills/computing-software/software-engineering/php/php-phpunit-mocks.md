---
id: computing-software.software-engineering.php.php-phpunit-mocks
name: php-phpunit-mocks
category: computing-software
field: software-engineering
product: php
tags: [php, php-testing-analysis, phpunit-mocks]
level: practitioner
status: draft
description: "Create stubs and mocks with createMock and verify interactions sparingly."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test doubles with PHPUnit mocks and Mockery
- `$repo = $this->createStub(Repo::class); $repo->method('find')->willReturn($x);` vs `createMock` + `expects($this->once())->method(...)->with(...)`.
- Cannot mock final classes by default; prefer interfaces. Avoid mocking value objects.
- Use in-memory fakes for repositories.
Verify: tests fail when you break the verified behaviour.
