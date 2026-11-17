---
id: computing-software.software-engineering.perl.dbi-connect-prepare-fetch
name: dbi-connect-prepare-fetch
category: computing-software
field: software-engineering
product: perl
tags: [perl, dbi, placeholders, prepare-execute, selectall-arrayref, dbd-drivers, dbi-connect-prepare-fetch, perl-database]
level: practitioner
status: draft
description: "Connect with DBI, use placeholders for every value, choose fetch methods, and set RaiseError and encoding options."
sources: ["https://metacpan.org/pod/DBI", "https://metacpan.org/pod/DBI::DBD"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DBI connect, prepare, placeholders and fetching

**Goal:** safe, idiomatic database access.

```perl
use DBI;
my $dbh = DBI->connect($dsn, $user, $pass, {
    RaiseError => 1,  PrintError => 0,  AutoCommit => 1,
    # driver specific: mysql_enable_utf8mb4 => 1, pg_enable_utf8 => 1, sqlite_unicode => 1
}) or die $DBI::errstr;
# DSNs: "dbi:Pg:dbname=app;host=db", "dbi:mysql:database=app;host=db", "dbi:SQLite:dbname=/path/file.db"

my $rows = $dbh->selectall_arrayref('SELECT id, name FROM users WHERE age > ? AND status = ?', { Slice => {} }, $min, 'active');
my ($n) = $dbh->selectrow_array('SELECT count(*) FROM users');
my $row  = $dbh->selectrow_hashref('SELECT * FROM users WHERE id = ?', undef, $id);
my $sth = $dbh->prepare('INSERT INTO log (msg, at) VALUES (?, ?)');   # prepare once...
$sth->execute($_, time) for @msgs;                                     # ...execute many
while (my $r = $sth->fetchrow_hashref) { ... }
$dbh->do('UPDATE t SET x = ? WHERE id = ?', undef, $x, $id);           # returns rows affected ("0E0" if none)
my $id = $dbh->last_insert_id(undef, undef, 'users', 'id');            # driver dependent
$dbh->disconnect;
```

## Rules
- **Always use placeholders** (`?` or `:name`) for values: it prevents SQL injection and enables statement reuse. Identifiers (table/column names) cannot be placeholders: whitelist them or use `$dbh->quote_identifier`.
- `$dbh->quote($v)` exists but placeholders are preferred.
- `RaiseError => 1` makes failures die; use eval/try; leave `PrintError` off to avoid double reporting.
- `selectall_hashref($sql, 'id')`, `selectcol_arrayref` cover other shapes; `fetchall_arrayref({})` returns hashes; `bind_columns` is the fastest fetch.
- `IN (?, ?, ?)`: build `join ',', ('?') x @ids`.
- Column names in returned hashes are driver-case dependent; set `FetchHashKeyName => 'NAME_lc'`.
- NULL is `undef`; compare with `IS NULL`, not `= ?` with undef.
- `$dbh->{Profile}` / `DBI_PROFILE=2` environment variable profiles query time.
- `DBI->available_drivers` lists drivers; install matching `DBD::*` (needs client libraries).

## Failure modes
- Connection reuse after fork: set `InactiveDestroy` in the child.
- Forgetting `finish` on a partially read statement before disconnect gives warnings.

## Self-check
- [ ] A query built with a hostile string `' OR 1=1 --` as a placeholder value returns zero rows.
