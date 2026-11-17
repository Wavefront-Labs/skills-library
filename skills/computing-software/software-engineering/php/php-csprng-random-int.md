---
id: computing-software.software-engineering.php.php-csprng-random-int
name: php-csprng-random-int
category: computing-software
field: software-engineering
product: php
tags: [php, csprng-random-int, security]
level: intro
status: docs-checked
description: "Choose the right PHP randomness: random_bytes and random_int for secrets, mt_rand and the Randomizer class for non-security uses."
sources: ["https://www.php.net/manual/en/function.random-int.php", "https://www.php.net/manual/en/function.random-bytes.php", "https://www.php.net/manual/en/function.mt-rand.php", "https://www.php.net/manual/en/class.random-randomizer.php", "https://www.php.net/manual/en/function.uniqid.php", "https://www.php.net/manual/en/function.hash-equals.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure random numbers

```php
$token = bin2hex(random_bytes(32));         // 64 hex chars from 32 CSPRNG bytes
$code  = random_int(100000, 999999);        // uniform integer from the closed interval [min, max]
$pick  = $items[random_int(0, count($items) - 1)];

// PHP 8.2+ ext-random
$r = new Random\Randomizer();
$r->shuffleArray($items); $r->pickArrayKeys($items, 2); $r->getInt(1, 6);
$seeded = new Random\Randomizer(new Random\Engine\Mt19937(42));  // repeatable, NOT secret
```
`random_bytes()` and `random_int()` are backed by the operating system's CSPRNG. Use them for session ids, CSRF tokens, reset links, API keys, salts and OTP codes. For a secure `Randomizer`, pass the `Random\Engine\Secure` engine explicitly.

## Gotchas
- `mt_rand()`, `rand()`, `shuffle()`, `lcg_value()` and `uniqid()` state that they are not cryptographically secure and must not be used for security purposes; `uniqid()` is time-based.
- Seeding `mt_srand()`/`srand()` with a known value produces a repeatable sequence; seeded engines are for tests and simulations.
- `random_bytes()` throws `Random\RandomException` (a plain `Exception` before PHP 8.2) when no randomness source is available, and `ValueError` for a length below 1. Do not catch and fall back to weak randomness.
- Compare secrets with `hash_equals()` (timing-safe), not `==`.

Verify: check the token length, e.g. `strlen($token) === 64`, and review security paths for `mt_rand`/`rand` uses.

## Checked
2026-11-03. Confirmed on the random_int, random_bytes, mt_rand, shuffle, lcg_value, uniqid, Random\Randomizer and Mt19937 manual pages. Removed (not confirmed on pages read): modulo-bias example, hashing tokens at rest, minimum token lengths, the `rand()`-adjacent claims for `array_rand` and `str_shuffle`.
Method: documentation only; no commands were run.
