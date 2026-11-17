---
id: computing-software.web-development.phoenix.scopes
name: scopes
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, scope, currentscope, authorization, generators, config, multi-tenant, elixir]
level: advanced
status: docs-checked
description: "Configure and extend Phoenix scopes: config :scopes options, custom scope modules, organization scopes with route_prefix, and scoped generators."
sources:
  - https://hexdocs.pm/phoenix/scopes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep every data operation tied to the current user/team/organization (guarding against broken access control).

A scope is a struct holding request/session info (user, organization, permissions, IP...). `mix phx.gen.auth` generates one and sets it as default if none exists. Router `scope` and `current_scope` are different features at different layers (router vs data).

## How generated code uses it

With a default scope configured, `phx.gen.html/json/live/context/schema` produce scoped resources: context functions take the scope first (`Blog.list_posts(socket.assigns.current_scope)`), filtering like `where: post.user_id == ^scope.user.id`, and LiveViews subscribe to scoped PubSub. LiveView routes must sit inside an authenticated `live_session`. The scope is assigned by the `fetch_current_scope_for_user` plug (`:browser` pipeline) or the `:mount_current_scope` on_mount hook. Pick a non-default scope with `--scope organization`.

## Scope config options

```elixir
config :my_app, :scopes,
  user: [
    default: true,
    module: MyApp.Accounts.Scope,
    assign_key: :current_scope,
    access_path: [:user, :id],
    schema_key: :user_id,
    schema_type: :id,
    schema_table: :users,
    test_data_fixture: MyApp.AccountsFixtures,
    test_setup_helper: :register_and_log_in_user
  ]
```

- `default`: only one scope can be default.
- `module`, `assign_key`: scope struct and where it is assigned on conn/socket.
- `access_path`: path to the identifying field (generates `scope.user.id`).
- `route_prefix` (optional): e.g. `/organizations/:org`; `route_access_path` (optional) picks the value for the URL, e.g. a slug (defaults to `access_path` minus last key).
- `schema_key`, `schema_type`, `schema_table`: foreign key on scoped schemas; `schema_migration_type` (optional) sets the migration column type.
- `test_data_fixture`: must define `NAME_scope_fixture/0` (e.g. `user_scope_fixture/0`); `test_setup_helper`: a `setup` function usually in `ConnCase`.

## Custom scope example (per session)

Define `defstruct id: nil` plus `for_id/1`; add a plug `assign_scope` in `:browser` that stores `:scope_id` in the session and assigns `:current_scope`; add a fixture and a `ConnCase` helper using `init_test_session` and `put_session`; configure `session: [default: true, module: MyApp.Scope, access_path: [:id], schema_key: :session_id, schema_type: :id, schema_migration_type: :bigint, schema_table: nil, ...]`. `schema_table: nil` stores a plain `bigint` instead of a foreign key. Then `mix phx.gen.html Post posts title:string`; a post copied into another session raises `Ecto.NoResultsError` (404 when `debug_errors` is off).

## Augmenting with organizations

Extend the struct (`defstruct user: nil, organization: nil`) with `put_organization/2`; add a plug `assign_org_to_scope` (reads `conn.params["org"]`, loads via `get_organization_by_slug!(current_scope, slug)`) and a matching `on_mount(:assign_org_to_scope, ...)` added to the `live_session` `on_mount` list. That lookup must filter by what the current scope can access. Add an `organization:` entry (`access_path: [:organization, :id]`, `route_prefix: "/organizations/:org"`, `route_access_path: [:organization, :slug]`, `schema_key: :org_id`, `schema_table: :organizations`, plus fixtures/helper), then `mix phx.gen.live Blog Post posts title:string body:text --scope organization`. Organization schemas can `@derive {Phoenix.Param, key: :slug}`.

## Helpers

Add a `Scope.for(opts)` helper (building from `user:` and `org:` ids/emails/slugs), alias `Scope` in `.iex.exs`, then call `MyApp.Blog.list_posts(Scope.for(user: 1, org: "foo"))` in IEx.

Related: computing-software.web-development.phoenix.gen-auth, computing-software.web-development.phoenix.cross-context

## Checked

2026-11-08. Confirmed against the Phoenix guide source (phoenixframework/phoenix, guides/authn_authz/scopes.md, main branch, read in full), the published form of the cited hexdocs page: every scope config option, the phx.gen.auth scope code, the custom session scope and organization examples, route_access_path default and scope helpers. Removed: the claim that a generator run can opt out with --no-scope (not in the guide).

Method: documentation only; no commands were run.
