---
id: computing-software.database-administration.postgresql.pgcrypto-hashing-and-encryption
name: pgcrypto-hashing-and-encryption
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pgcrypto, crypt, gen-salt, pgp-sym-encrypt, column-encryption, password-hashing, security]
level: practitioner
status: verified
description: "Use pgcrypto in PostgreSQL for bcrypt password hashing, PGP column encryption and random bytes, and avoid leaking keys through logs and pg_stat_statements."
sources:
  - https://www.postgresql.org/docs/current/pgcrypto.html
  - https://www.postgresql.org/docs/current/functions-uuid.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pgcrypto hashing and encryption functions

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

## Password hashing (bcrypt)
```sql
INSERT INTO users (email, pw_hash) VALUES ($1, crypt($2, gen_salt('bf', 12)));
SELECT id FROM users WHERE email = $1 AND pw_hash = crypt($2, pw_hash);
```
- `gen_salt('bf', 12)`: bcrypt with cost 12 (produces `$2a$12$...`); the allowed range is 4 to 31 (default 6; 3 and 32 raise `gen_salt: Incorrect number of rounds`); raise the cost as hardware gets faster. Never use `md5()`/`sha256()` for passwords.
- Better practice is to hash in the application (argon2id) so plaintext never reaches the DB server, its logs or replicas.

## Hashes / HMAC
```sql
SELECT encode(digest('data', 'sha256'), 'hex');
SELECT encode(hmac('payload', '<KEY>', 'sha256'), 'hex');
```
`sha224()`, `sha256()`, `sha384()` and `sha512()` are built in since PG11 without pgcrypto (same output as `digest(..., 'sha256')` here).

## Symmetric column encryption (PGP)
```sql
UPDATE patients SET ssn_enc = pgp_sym_encrypt(ssn, current_setting('app.enc_key'), 'cipher-algo=aes256');
SELECT pgp_sym_decrypt(ssn_enc, current_setting('app.enc_key')) FROM patients WHERE id = 1;
```
Column type `bytea`. Set the key per session from the app (`SET app.enc_key = ...` over TLS), never store it in the database.

## Random values
```sql
SELECT encode(gen_random_bytes(32), 'base64');   -- tokens
SELECT gen_random_uuid();                         -- built in since PG13, no extension needed
```

## Key leakage paths (the real risk)
- Keys/plaintext in SQL text land in: server logs (`log_statement`, `log_min_duration_statement`, error messages), `pg_stat_statements` (constants are normalised there, but not in logs), `pg_stat_activity.query`.
- Use bind parameters, disable statement logging for the role (`ALTER ROLE app SET log_statement = 'none'`), restrict `log_min_error_statement`.
- Encrypted columns cannot be indexed for search; store an HMAC blind index alongside for equality lookups.

## Gotchas
- `pgp_sym_decrypt` with a wrong key raises `Wrong key or corrupt data`; wrap in exception handling in batch jobs.
- Encryption in SQL means the DB server sees plaintext; for threat models including DBAs, encrypt client-side.
- With OpenSSL 3 the legacy provider must be enabled in `openssl.cnf` to use older ciphers such as DES or Blowfish (the `cipher-algo=bf` option of the PGP functions, `encrypt(..., 'bf')`); in FIPS mode `pgcrypto.builtin_crypto_enabled` (PG17) controls whether the built-in `crypt()` and `gen_salt()` work. `fips_mode()` reports the state.

## Checked
PostgreSQL 17.6: `crypt(pw, gen_salt('bf',12))` returns a `$2a$12$` hash and `crypt('pw', hash) = hash` is true (false for a wrong password); `gen_salt('bf',3)` and `32` error; `digest('data','sha256')` equals built-in `sha256('data')`; `hmac`, `gen_random_bytes(32)` (44 base64 characters) and `gen_random_uuid()` run; `pgp_sym_encrypt` returns `bytea`, decrypts with the right key and raises `Wrong key or corrupt data` with a wrong one. Docs (pgcrypto, release 11 and 13 notes): iteration-count table, SHA-2 functions added in 11, `gen_random_uuid()` added in 13, OpenSSL 3 legacy provider note. With `log_statement = 'all'` a key passed as a literal appeared in the server log, `ALTER ROLE app SET log_statement = 'none'` stopped that for the role, but a failing statement (wrong function arguments) still logged its full text including the key via the error `STATEMENT:` line; `pg_stat_statements` replaces constants with `$1` (PG docs).
