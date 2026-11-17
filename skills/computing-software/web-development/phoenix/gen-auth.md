---
id: computing-software.web-development.phoenix.gen-auth
name: gen-auth
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, authentication, phxgenauth, magiclink, sudomode, scope, security, elixir]
level: practitioner
status: docs-checked
description: "Generate authentication with mix phx.gen.auth: setup steps, generated plugs, hashing options, notifiers and the page's security caveats."
sources:
  - https://hexdocs.pm/phoenix/mix_phx_gen_auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add registration, login and session handling by generating code into your app.

Features: registration with email confirmation, log in with magic links, opt-in password authentication, and "sudo mode" (re-confirm identity before sensitive actions).

## Run it

Commit first, since many files are generated.

```console
$ mix phx.gen.auth Accounts User users
```

Args: context, schema, plural table name. It makes an `Accounts` context with `User` and `UserToken` schemas. It asks `Do you want to create a LiveView based authentication system? [Y/n]`; either answer gives the same context, schemas, tables and routes. Then:

```console
$ mix deps.get
$ mix ecto.migrate
$ mix test
$ mix phx.server
```

Register and Log in links appear on the default page.

## Generated pieces

`MyAppWeb.UserAuth` plugs:
- `fetch_current_scope_for_user` - stores `:current_scope` assign
- `require_authenticated_user` - run after the fetch plug
- `redirect_if_user_is_authenticated` - controller-based variant only
- `require_sudo_mode` - recent-authentication check for sensitive pages

LiveView variants are `:on_mount` hooks. A scope module `lib/my_app/accounts/scope.ex` (struct with `user`, `for_user/1`) is generated; later generator runs pass it to context functions (see the scopes skill).

Password hashing defaults to `bcrypt` on Unix and `pbkdf2` on Windows (Comeonin interface); override with `--hashing-lib bcrypt|pbkdf2|argon2`. The page recommends `argon2` as most robust, but it is CPU and memory intensive.

Notifiers send nothing real: they log a message to the terminal; integrating email/SMS is your job. With `phx.new`'s default Swoosh mailer, view dev emails at `/dev/mailbox`.

## Responsibilities and security notes

- Generated code is yours and is not updated later; security fixes are flagged in `CHANGELOG.md` and upgrade notes.
- Sessions and tokens live in a separate table; changing a password deletes all tokens, forcing re-login everywhere.
- No protection against user enumeration (registering an existing email says so) or timing attacks; build your own flow if sensitive.
- Unconfirmed accounts are forbidden from using the app by default.
- Email lookup is case-insensitive; on PostgreSQL via the `citext` extension (the generator creates it). If migrating fails because it is split out, installing `postgres-contrib` most likely fixes it.

Related: computing-software.web-development.phoenix.scopes

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
