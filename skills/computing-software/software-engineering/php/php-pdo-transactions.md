---
id: computing-software.software-engineering.php.php-pdo-transactions
name: php-pdo-transactions
category: computing-software
field: software-engineering
product: php
tags: [php, pdo-transactions, database]
level: practitioner
status: docs-checked
description: "Use PDO error modes, transactions, rollback, DDL implicit commits and the emulated-prepares attribute correctly."
sources: ["https://www.php.net/manual/en/pdo.transactions.php", "https://www.php.net/manual/en/pdo.error-handling.php", "https://www.php.net/manual/en/pdo.setattribute.php", "https://www.php.net/manual/en/pdo.begintransaction.php", "https://www.php.net/manual/en/pdo.constants.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDO transactions and error modes

```php
$pdo = new PDO($dsn, $user, $pass, [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,   // default as of PHP 8.0.0
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,                    // ask for native prepared statements
]);

function transfer(PDO $pdo, int $from, int $to, int $cents): void {
    $attempts = 0;
    while (true) {
        try {
            $pdo->beginTransaction();
            $pdo->prepare('UPDATE accounts SET bal = bal - ? WHERE id = ? AND bal >= ?')->execute([$cents, $from, $cents]);
            $pdo->prepare('UPDATE accounts SET bal = bal + ? WHERE id = ?')->execute([$cents, $to]);
            $pdo->commit();
            return;
        } catch (PDOException $e) {
            if ($pdo->inTransaction()) { $pdo->rollBack(); }
            // isRetryable(): your own check of $e->errorInfo (SQLSTATE, driver code, message) for deadlock/lock-wait
            if (!isRetryable($e) || ++$attempts >= 3) { throw $e; }
        }
    }
}
```

## What the manual states
- Error modes: `ERRMODE_SILENT` (error code only; the default before PHP 8.0.0), `ERRMODE_WARNING` (also an `E_WARNING`), `ERRMODE_EXCEPTION` (throws `PDOException`; the default as of 8.0.0). `PDO::__construct()` always throws `PDOException` on a failed connection, whatever the mode.
- `errorCode()` returns one SQLSTATE; `errorInfo()` returns an array with the SQLSTATE, the driver-specific error code and the driver-specific message. Drivers map native codes to SQLSTATE.
- PDO starts in auto-commit mode: each query is its own implicit transaction (if the database supports transactions). `beginTransaction()` starts one; `commit()` or `rollBack()` ends it. If the driver does not support transactions, `beginTransaction()` throws `PDOException` regardless of the error mode.
- `beginTransaction()` throws `PDOException` if a transaction is already started, so PDO has no nested transactions of its own.
- PDO checks transaction support only at driver level: on MySQL with MyISAM tables `beginTransaction()` still returns true.
- If a script ends or the connection closes with an outstanding transaction begun through `beginTransaction()`, PDO rolls it back automatically. A transaction started by a manually issued query is not rolled back by PDO.
- `PDO::ATTR_EMULATE_PREPARES` is available for the OCI, Firebird and MySQL drivers. True always emulates prepares; otherwise PDO tries native prepares and falls back to emulation if the driver cannot prepare the query. For the MySQL driver the constants page describes emulation as on by default.
- `PDO::ATTR_AUTOCOMMIT` (OCI, Firebird, MySQL only) defaults to true.
- `PDO::ATTR_TIMEOUT` is seconds as an int; not all drivers support it and its meaning varies (SQLite waits that long for a writable lock; others treat it as a connection or read timeout).

## Gotchas
- DDL (`CREATE TABLE`, `DROP TABLE`) inside a transaction triggers an implicit COMMIT on some databases; the manual names MySQL and Oracle. Earlier changes cannot then be rolled back, and a later `rollBack()` will not undo them. Keep DDL out of transactions on those databases.
- Always roll back on every failure path; use `inTransaction()` before `rollBack()` as above.
- `ERRMODE_SILENT` only sets error codes, so check return values if you use it.
- The manual's claim that no one else can change data while your transaction runs is only as strong as the isolation level and locking reads you use; check your database server's documentation (a reader note on that page points out `SELECT ... FOR UPDATE`).
- `setAttribute()` returns false rather than throwing on failure.
- Keep transactions short and avoid network calls inside them.
- Never put identifiers (table or column names) in placeholders; whitelist them.

Verify: force a failure on the second statement and confirm the first update is rolled back.

## Checked
Confirmed 2026-11-08 against the PHP manual pages for PDO transactions and auto-commit, errors and error handling, PDO::setAttribute, PDO::beginTransaction and PDO predefined constants. Removed as not stated by those pages: MySQL error numbers 1213/1205 for deadlock and lock wait, the "native types" claim for disabled emulation, SAVEPOINT usage, `rowCount()` and `PDO::MYSQL_ATTR_FOUND_ROWS` behaviour, and persistent-connection transaction advice. The retry check is now a placeholder.
Method: docs-only read of cited pages, 2026-11-08
