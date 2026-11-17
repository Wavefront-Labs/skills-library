---
id: computing-software.web-development.rails.active-record-encryption
name: active-record-encryption
category: computing-software
field: web-development
product: rails
tags: [rails, active-record-encryption, encrypts, deterministic-encryption, key-rotation, pii, ruby, web-development]
level: practitioner
status: docs-checked
description: "Encrypting sensitive columns with Active Record encryption: key setup, encrypts with deterministic vs random modes, querying, migrating existing data and key rotation."
sources:
  - https://guides.rubyonrails.org/active_record_encryption.html
  - https://guides.rubyonrails.org/security.html#custom-credentials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active Record encryption

**Goal:** PII and secrets encrypted at the application layer, so DB dumps, backups and read replicas don't leak plaintext.

## 1. Keys
```bash
bin/rails db:encryption:init        # prints primary_key, deterministic_key, key_derivation_salt
bin/rails credentials:edit --environment production
```
```yaml
active_record_encryption:
  primary_key: ...
  deterministic_key: ...
  key_derivation_salt: ...
```
Different keys per environment; losing them means losing the data. Back them up in a secret manager.

## 2. Declare encrypted attributes
```ruby
class User < ApplicationRecord
  encrypts :ssn                                    # non-deterministic (random IV): strongest, can't query
  encrypts :email, deterministic: true, downcase: true   # same input -> same ciphertext: queryable, leaks equality
  encrypts :notes, compress: false                 # compression is on by default; opt out per attribute
end
User.find_by(email: "a@example.com")              # works only with deterministic
```
Columns need room for ciphertext plus metadata: the guide estimates worst-case overhead of about 255 bytes and recommends, for example, `string(510)` for a `string(255)` email column and `string(2000)` for a `string(500)` non-western text column. Use `text` when unsure.

## 3. Trade-offs
- Deterministic encryption allows equality lookups and unique indexes but reveals which rows share a value. Use only where you must query.
- Deterministic encryption only supports exact-match queries such as `WHERE title = "..."`; do not rely on `LIKE`, range or ordering queries against encrypted columns.
- Params named like encrypted attributes are filtered from the Rails logs automatically.
- Without a `deterministic_key`, deterministic encryption is effectively disabled. `ignore_case: true` preserves the original case but needs an `original_<attribute>` column.

## 4. Encrypting existing data
```ruby
config.active_record.encryption.support_unencrypted_data = true      # transitional: read plaintext rows
config.active_record.encryption.extend_queries = true                # deterministic queries match both forms
User.find_each(&:encrypt)                                            # backfill (in batches / a job)
```
Both options default to `false`, the recommended long-term setting; turn them off once the backfill is complete.

## 5. Key rotation
`primary_key` accepts a list (credentials `primary_key: [old, new]`): the **last** key encrypts new content and every key is tried when decrypting. Add the new key at the end, re-encrypt rows with `record.encrypt`, then remove the old key. The guide notes that rotating keys is not supported for deterministic encryption. Changing an attribute's scheme (for example deterministic to non-deterministic) is handled with `previous:` encryption schemes plus `extend_queries`.

## 6. Fixtures and tests
`config.active_record.encryption.encrypt_fixtures = true` encrypts test fixtures. `record.ciphertext_for(:ssn)` returns the stored ciphertext and `record.encrypted_attribute?(:ssn)` checks whether an attribute is encrypted; raw SQL on the column should show ciphertext, not plaintext.

## Verify
- [ ] Raw SQL shows ciphertext JSON, not plaintext, for encrypted columns.
- [ ] Lookups on deterministic columns still work; encrypted fields absent from logs.
- [ ] Production keys stored outside the repo and in a backup location.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Active Record Encryption guide. Confirmed: `bin/rails db:encryption:init` and the three key names, `encrypts` with `deterministic:`, `downcase:` and `ignore_case:`, compression on by default, storage overhead and recommended column sizes, `support_unencrypted_data` and `extend_queries` (both default false), `previous:` schemes, key lists where the last key encrypts, `encrypt_fixtures`, `encrypt`, `ciphertext_for` and log parameter filtering. Fixed: `compress: true` is the default, not an option to add; the guide states that key rotation is not supported for deterministic encryption; removed the HMAC-digest search suggestion.

Method: documentation only; no commands were run.
