---
id: computing-software.database-administration.schema-design.text-length-limits-and-unicode
name: text-length-limits-and-unicode
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, varchar-length, text-columns, unicode, utf8mb4, collation, data-types]
level: practitioner
status: gated
description: "Choose text column types and length limits (varchar(n) vs text, nvarchar, utf8mb4) per engine, count characters vs bytes correctly, and avoid truncation and index-size limits."
sources:
  - https://www.postgresql.org/docs/current/datatype-character.html
  - https://dev.mysql.com/doc/refman/8.4/en/charset-unicode-utf8mb4.html
  - https://learn.microsoft.com/en-us/sql/t-sql/data-types/char-and-varchar-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text length limits (varchar(n) vs text) and Unicode

## Engine facts
| Engine | Notes |
|---|---|
| PostgreSQL | `text` and `varchar(n)` have identical storage/performance; `n` is only a constraint (characters). `char(n)` pads; avoid it |
| MySQL | `VARCHAR(n)` counts characters; row size limit 65,535 bytes across columns; `TEXT` stored off-page, cannot have defaults before 8.0.13, index needs prefix length. Use `utf8mb4` (real UTF-8), never `utf8`/`utf8mb3` (no emoji) (gated: unconfirmed, source is paywalled or blocked) |
| SQL Server | `varchar(n)` counts **bytes** in its code page; `nvarchar(n)` is the UTF-16 type; `(max)` for > 8000 bytes. 2019+ UTF-8 collations (`_UTF8`) let `varchar` store Unicode |
| Oracle | `VARCHAR2(n BYTE)` vs `(n CHAR)`: set `NLS_LENGTH_SEMANTICS=CHAR` or declare CHAR; max 4000 bytes (32767 with `MAX_STRING_SIZE=EXTENDED`) (gated: unconfirmed, source is paywalled or blocked) |
| SQLite | Declared lengths are ignored (no enforcement) unless you add CHECK (gated: unconfirmed, source is paywalled or blocked) |

## Choosing limits
- Use a limit when the domain has one (ISO country code `char(2)`/`text CHECK (length = 2)`, phone numbers, SKU formats) and validate format with CHECK.
- For free text (names, addresses, descriptions) generous limits or `text` + CHECK on a sane maximum (`CHECK (length(bio) <= 5000)`) protect against abuse without arbitrary truncation. Names: do not assume 50 chars or ASCII.
- Changing `varchar(50)` to `varchar(100)`: cheap metadata change in PostgreSQL and MySQL (within the same length-byte class: crossing 255 bytes in MySQL forces a copy); shrinking requires a scan/rewrite (gated: unconfirmed, source is paywalled or blocked).

## Characters vs bytes
A 4-byte emoji or a CJK character in UTF-8 counts as one character but 3-4 bytes. Byte-limited types (SQL Server `varchar`, Oracle BYTE semantics, MySQL index key limits) truncate or reject earlier than expected. Grapheme clusters (emoji with modifiers, combining accents) can be several code points: user-visible "length" differs again.

## Normalisation and comparison
Store Unicode in NFC so equal-looking strings compare equal (PostgreSQL has a `normalize()` function (gated: unconfirmed, source is paywalled or blocked)). Case-insensitive matching needs proper collations (ICU, `_ci` collations) rather than `lower()` for non-ASCII.

## Index limits
Index key size limits differ by engine (InnoDB, SQL Server nonclustered keys, PostgreSQL B-tree entries): look up the current limits in each engine's docs (gated: unconfirmed, source is paywalled or blocked); index a hash or prefix for long text.

## Verify
Insert test strings with emoji, CJK and combining characters into each text column; confirm they round-trip unchanged through the application and that length constraints behave as specified.

## Checked

Date: 2026-11-02. Confirmed on PostgreSQL docs (character types: text and varchar(n) have no performance difference, char(n) is blank-padded) and Microsoft Learn char/varchar (varchar(n) counts bytes, (max), SQL Server 2019 UTF-8 collations). Removed as not stated there: nvarchar byte-pair wording, exact index-key byte limits (3072, 1700, ~2700, 768 chars). Left, marked gated: MySQL (docs blocked to fetch), Oracle, SQLite, schema-change cost and normalize() claims.

Method: documentation only; no commands were run.
