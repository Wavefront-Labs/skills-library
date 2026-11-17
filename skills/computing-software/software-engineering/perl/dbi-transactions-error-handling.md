---
id: computing-software.software-engineering.perl.dbi-transactions-error-handling
name: dbi-transactions-error-handling
category: computing-software
field: software-engineering
product: perl
tags: [perl, dbi-transaction, begin-work, rollback, connect-cached, savepoint, dbi-transactions-error-handling]
level: advanced
status: draft
description: "Wrap multi-statement changes in DBI transactions with begin_work/commit/rollback, handle errors, retry on deadlock and manage connections."
sources: ["https://metacpan.org/pod/DBI"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transactions, error handling and connection reuse

**Goal:** atomic units of work.

```perl
$dbh->begin_work;                                 # turns AutoCommit off until commit/rollback
eval {
    $dbh->do('UPDATE acct SET bal = bal - ? WHERE id = ?', undef, $amt, $from);
    $dbh->do('UPDATE acct SET bal = bal + ? WHERE id = ?', undef, $amt, $to);
    $dbh->commit;
    1;
} or do {
    my $err = $@ || 'unknown';
    eval { $dbh->rollback };
    die "transfer failed: $err";
};
```
Alternative connection style: `AutoCommit => 0` then call `commit` explicitly; with `RaiseError` an exception leaves the transaction open until you roll back.

## Rules
- `begin_work` dies if AutoCommit is already off; do not nest. Use savepoints via `$dbh->do('SAVEPOINT s1')` where the database supports them, or DBIx::Class `txn_do` (see below).
- Retry transient failures (deadlock, serialization failure) a limited number of times with backoff, after a rollback.
- `$dbh->ping` checks liveness; `DBI->connect_cached` reuses by arguments (reconnects silently on dead handles in some drivers); pooling libraries (Mojo::Pg, `DBIx::Connector`) manage reconnection and forks.
- `DBIx::Connector->new(...)->txn(fixup => sub { ... })` retries once if the connection dropped.
- Set `$dbh->{HandleError}` for central error mapping; `$dbh->err`/`errstr` expose driver codes (use SQLSTATE `state`).
- After `fork`, child must not use the parent's `$dbh`; reconnect.
- Long transactions hold locks; keep them short and avoid user interaction inside them.
- Isolation level: `$dbh->do('SET TRANSACTION ISOLATION LEVEL ...')` (database specific).

## Failure modes
- Exception thrown after partial work with no rollback leaves the connection in an aborted state (PostgreSQL: "current transaction is aborted").
- `commit` under AutoCommit => 1 warns "commit ineffective with AutoCommit enabled".

## Self-check
- [ ] A forced failure on the second UPDATE leaves both balances unchanged.
