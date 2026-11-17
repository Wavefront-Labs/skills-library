---
id: computing-software.software-engineering.php.php-pdo-prepared-statements
name: php-pdo-prepared-statements
category: computing-software
field: software-engineering
product: php
tags: [php, php-security, pdo-prepared-statements]
level: practitioner
status: docs-checked
description: "Prevent SQL injection with PDO prepared statements, correct DSN options and error modes."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDO prepared statements
- `$pdo = new PDO($dsn, $u, $p, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_EMULATE_PREPARES => false, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);`
- `$st = $pdo->prepare('SELECT * FROM t WHERE id = :id'); $st->execute(['id' => $id]);` Identifiers and ORDER BY columns cannot be bound: whitelist them.
- Set charset in DSN (`charset=utf8mb4` for MySQL).
- `IN (...)` needs generated placeholders.
Verify: attempt `' OR 1=1 --` as input in a test.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
