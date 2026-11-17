---
id: computing-software.web-development.rails.credentials-and-secrets
name: credentials-and-secrets
category: computing-software
field: web-development
product: rails
tags: [rails, rails-credentials, master-key, secrets, encrypted-credentials, rails-master-key, ruby, web-development]
level: practitioner
status: docs-checked
description: "Managing Rails secrets with encrypted credentials: per-environment files and keys, RAILS_MASTER_KEY in deploys, access patterns, rotation and merge conflicts."
sources:
  - https://guides.rubyonrails.org/security.html#custom-credentials
  - https://guides.rubyonrails.org/configuring.html#config-require-master-key
  - https://guides.rubyonrails.org/asset_pipeline.html
  - https://github.com/rails/rails/blob/v8.1.4/railties/lib/rails/commands/credentials/USAGE
  - https://github.com/rails/rails/blob/v8.1.4/railties/lib/rails/commands/credentials/credentials_command.rb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credentials and secrets

**Goal:** secrets versioned safely with the app, decryptable only where needed, and failing loudly when missing.

## 1. Files
```bash
EDITOR="code --wait" bin/rails credentials:edit                          # config/credentials.yml.enc + config/master.key
EDITOR="code --wait" bin/rails credentials:edit --environment production # config/credentials/production.yml.enc + production.key
bin/rails credentials:show --environment production
```
Encrypted files are committed; the key must not be (the Rails USAGE text says to add `config/master.key` to your ignore file and that Rails handles this for Git; check your repo). An environment-specific file created with `--environment` takes precedence over the global `config/credentials.yml.enc` in that environment, with its key in `config/credentials/<env>.key`. `config.credentials.content_path` and `config.credentials.key_path` override the lookup paths.

## 2. Contents and access
```yaml
aws:
  access_key_id: AKIA...
  secret_access_key: ...
stripe_secret_key: sk_live_...
secret_key_base: ...
```
```ruby
Rails.application.credentials.aws[:access_key_id]
Rails.application.credentials.dig(:aws, :secret_access_key)
Rails.application.credentials.stripe_secret_key!     # bang raises KeyError if blank
Rails.application.credentials.fetch(:stripe_secret_key)   # Hash-style access
```
Use bang/fetch for required secrets so boot fails instead of nil errors at request time.

## 3. Deploy
Provide the key via the `RAILS_MASTER_KEY` environment variable, which takes precedence over `config/master.key` and over environment-specific key files (deployment configuration, CI secrets or container env). Set `config.require_master_key = true` in production so the app does not boot without a master key. Build steps that precompile assets can set `SECRET_KEY_BASE_DUMMY=1` (`RAILS_ENV=production SECRET_KEY_BASE_DUMMY=1 rails assets:precompile`) to use a random temporary `secret_key_base` instead of the production secrets.

## 4. Credentials vs ENV
Credentials: secrets owned by developers, versioned, reviewed. ENV: values that differ per deployment, are managed by ops/platform, or rotate without a code change (DATABASE_URL from a managed DB). A common hybrid: `ENV.fetch("STRIPE_KEY") { Rails.application.credentials.stripe_secret_key! }`.

## 5. Rotation
- Rotating a secret value: edit credentials, deploy, revoke the old value at the provider.
- If secrets may have been exposed, change the secrets themselves; a lost master key cannot be recovered, and anyone holding it can read every secret in that file.
- Changing `secret_key_base` expires active sessions and requires all users to log in again; `config.action_dispatch.cookies_rotations` lets old cookie configurations (cipher or digest) still be read while they are upgraded.

## 6. Merge conflicts
`bin/rails credentials:diff --enroll` makes `git diff` show decrypted diffs of credentials files (a `rails_credentials` driver in `.gitattributes`); `--disenroll` removes it.

## Verify
- [ ] `git ls-files | grep "\.key$"` returns nothing.
- [ ] Production boots fail fast without `RAILS_MASTER_KEY`.
- [ ] Required secrets accessed with `!`/`fetch`.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 security, configuring and asset pipeline guides and the v8.1.4 credentials command USAGE and source. Confirmed: `credentials:edit`, `credentials:show`, `credentials:diff --enroll/--disenroll`, `--environment` override files and key paths, `RAILS_MASTER_KEY` precedence, `config.require_master_key`, `SECRET_KEY_BASE_DUMMY`, the bang accessor raising `KeyError`, hash-style `fetch`/`dig`, the expiry of sessions when `secret_key_base` changes and `cookies_rotations`. Removed the Kamal secrets line, the step-by-step master key rotation and the "replaces, no merging" wording, which the checked sources do not state.

Method: documentation only; no commands were run.
