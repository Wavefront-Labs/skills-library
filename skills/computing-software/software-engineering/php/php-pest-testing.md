---
id: computing-software.software-engineering.php.php-pest-testing
name: php-pest-testing
category: computing-software
field: software-engineering
product: php
tags: [php, pest-testing, testing, expectations]
level: practitioner
status: docs-checked
description: "Write Pest tests on PHPUnit: test/it/describe, the expectation API with chaining and not, and PHPUnit assertions."
sources: ["https://pestphp.com/docs/writing-tests", "https://pestphp.com/docs/expectations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pest testing

Pest is built on top of PHPUnit, so PHPUnit options and `phpunit.xml` configuration also apply to Pest tests.

Layout after install: `tests/Unit`, `tests/Feature`, `tests/TestCase.php` (shared setup), `tests/Pest.php` (suite configuration) and `phpunit.xml`. Test files are usually suffixed `Test.php`. Run with `./vendor/bin/pest`.

```php
// tests/Unit/SumTest.php
test('sum', function () {
    $result = sum(1, 2);
    expect($result)->toBe(3);
});

it('performs sums', function () {           // output reads "it performs sums"
    expect(sum(1, 2))->toBe(3);
});

describe('sum', function () {                // groups related tests
    it('may sum integers', fn () => expect(sum(1, 2))->toBe(3));
    it('may sum floats', fn () => expect(sum(1.5, 2.5))->toBe(4.0));
});

test('sum with phpunit assertions', function () {
    $this->assertSame(3, sum(1, 2));         // same as expect(...)->toBe(3)
});
```

Expectations chain on one value and `not` negates the next one:
```php
expect($value)->toBeInt()->toBe(3)->not->toBeString()->not->toBe(4);
```
Available expectations include `toBe`, `toEqual`, `toEqualWithDelta`, `toBeInstanceOf`, `toContain`, `toHaveCount`, `toHaveKey`, `toMatchArray`, `toBeNull` and `toThrow`. Modifiers include `and()`, `each()`, `json()`, `match()`, `not`, `sequence()`, `when()` and `unless()`.

## Gotchas
- `toBe` requires the same type and value (`expect('1')->not->toBe(1)`); with objects it requires the exact same object, so `expect(new StdClass())->not->toBe(new StdClass())`.
- You can mix the PHPUnit assertion API in when an expectation is not available.

Verify: run `./vendor/bin/pest` and confirm a deliberately failing expectation produces a failing result.

## Checked
2026-11-09. Rewritten from and confirmed against the Pest "Writing Tests" and "Expectations" pages. Removed because those pages do not state them: install and `--init` commands, `--filter`, `--parallel`, `--coverage --min` (Xdebug or PCOV), `beforeEach`, datasets and `->with()`, `arch()` tests, `->skip()`, snapshot testing, `toThrow` call form, closure binding and parallel-safety advice, and the PHPUnit/PHP version compatibility remark.
Method: documentation only; no commands were run.
