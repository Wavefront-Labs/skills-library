---
id: computing-software.web-development.phoenix.api-authentication
name: api-authentication
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, api-token, bearer, apitoken, authentication, plug, phx-gen-auth]
level: practitioner
status: docs-checked
description: "Add bearer API token authentication on top of mix phx.gen.auth: context functions, UserToken verification query, and an API pipeline plug."
sources:
  - https://hexdocs.pm/phoenix/api_authentication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: protect a Phoenix JSON API with bearer tokens stored in the token table that `mix phx.gen.auth` already created. Assumes `mix phx.gen.auth Accounts User users` was run (adapt names otherwise).

## 1. Context functions (`lib/my_app/accounts.ex`)

```elixir
def create_user_api_token(user) do
  {encoded_token, user_token} = UserToken.build_email_token(user, "api-token")
  Repo.insert!(user_token)
  encoded_token
end

def fetch_user_by_api_token(token) do
  with {:ok, query} <- UserToken.verify_api_token_query(token),
       %User{} = user <- Repo.one(query) do
    {:ok, user}
  else
    _ -> :error
  end
end
```

- The returned token cannot be recovered from the database, so it must be saved somewhere safe.
- It is an email token, so changing the user's email expires existing API tokens.
- The function is named `fetch_*` (returns `{:ok, user}` or `:error`) rather than `get_*` (usually `nil`) so the API can render different status codes.

## 2. Verification query (`lib/my_app/accounts/user_token.ex`)

Add a module attribute next to the others, e.g. `@api_token_validity_in_days 365` (validity is your choice; the guide uses 365 days), then:

```elixir
def verify_api_token_query(token) do
  case Base.url_decode64(token, padding: false) do
    {:ok, decoded_token} ->
      hashed_token = :crypto.hash(@hash_algorithm, decoded_token)

      query =
        from token in by_token_and_context_query(hashed_token, "api-token"),
          join: user in assoc(token, :user),
          where:
            token.inserted_at > ago(^@api_token_validity_in_days, "day") and
              token.sent_to == user.email,
          select: user

      {:ok, query}

    :error ->
      :error
  end
end
```

Without it, a test calling `fetch_user_by_api_token` fails with an UndefinedFunctionError for `verify_api_token_query/1`. The guide's test (in `test/my_app/accounts_test.exs`) asserts `Accounts.fetch_user_by_api_token(token) == {:ok, user}` for a fresh token and `:error` for `"invalid"`.

## 3. Plug (`lib/my_app_web/user_auth.ex`)

```elixir
def fetch_current_scope_for_api_user(conn, _opts) do
  with [<<bearer::binary-size(6), " ", token::binary>>] <-
         get_req_header(conn, "authorization"),
       true <- String.downcase(bearer) == "bearer",
       {:ok, user} <- Accounts.fetch_user_by_api_token(token) do
    assign(conn, :current_scope, Scope.for_user(user))
  else
    _ ->
      conn
      |> send_resp(:unauthorized, "No access for you")
      |> halt()
  end
end
```

## 4. Router

```elixir
pipeline :api do
  plug :accepts, ["json"]
  plug :fetch_current_scope_for_api_user
end
```

Clients send `authorization: Bearer TOKEN`, where TOKEN is the value from `Accounts.create_user_api_token/1`. Write plug tests in `test/my_app_web/user_auth_test.exs`, using the other plug tests as templates.

## Issuing tokens

- For your own JavaScript client: change `UserSessionController` to call `Accounts.create_user_api_token/1` and return the token in a JSON response.
- For third-party users: let them create tokens, show them the result of `create_user_api_token/1`, and tell them to store it safely and send it in the authorization header.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Removed an unsupported instruction about what to tell third-party users; the closing bullet now matches the page.

Method: documentation only; no commands were run.
