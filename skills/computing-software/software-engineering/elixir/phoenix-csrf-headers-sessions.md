---
id: computing-software.software-engineering.elixir.phoenix-csrf-headers-sessions
name: phoenix-csrf-headers-sessions
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, csrf, secure-browser-headers, cors, plug-security]
level: advanced
status: docs-checked
description: "Harden Phoenix apps: CSRF protection, secure headers, XSS, SQL injection, CORS, SSRF and access-control pitfalls from the Phoenix security guide."
sources: ["https://hexdocs.pm/phoenix/security.html", "https://hexdocs.pm/plug/Plug.CSRFProtection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSRF, headers, sessions and secrets in Phoenix

**Goal:** safe defaults for browser-facing Phoenix apps, from the Phoenix Security guide and `Plug.CSRFProtection`.

```elixir
# router: the default :browser pipeline
pipeline :browser do
  plug :accepts, ["html"]
  plug :fetch_session
  plug :protect_from_forgery      # checks the CSRF token
  plug :put_secure_browser_headers
end

# Plug.CSRFProtection used directly (needs a fetched session)
plug Plug.Session, ...
plug :fetch_session
plug Plug.CSRFProtection, with: :exception     # or :clear_session

# never decode untrusted binaries with :erlang.binary_to_term(x, [:safe])
Plug.Crypto.non_executable_binary_to_term(user_input, [:safe])
```

## Rules
- CSRF: `:protect_from_forgery` is in the default `:browser` pipeline. The token is sent as the `_csrf_token` param or the `x-csrf-token` header and compared with the token in the session; an invalid request raises `Plug.CSRFProtection.InvalidCSRFTokenError` (default `with: :exception`) or gets an empty session for that request (`with: :clear_session`).
- GET requests are not protected, so never change state in a GET action (including re-using a POST action for GET). `Plug.CSRFProtection` also forbids non-XHR GET JavaScript requests.
- Enable CSRF protection whenever a session is used, even for JSON requests. Call `delete_csrf_token/0` after login to avoid CSRF fixation. Use `get_csrf_token_for/1` for full URLs so the token is tied to the host; `:allow_hosts` lists extra hosts to accept.
- To skip protection in tests use `Plug.Conn.put_private(conn, :plug_skip_csrf_protection, true)`; for production routes use a different plug stack instead.
- Never pass user input to `Code.eval_string/3`, `System.cmd/3`, `:os.cmd/2` and similar. `:erlang.binary_to_term/2` with `:safe` does not stop executable terms; use `Plug.Crypto.non_executable_binary_to_term/2`.
- XSS: HEEx and `<%= %>` escape by default; never pass user input to `raw/1`, to `html/2` or `send_resp/3` HTML strings, or let users choose the content type of uploads.
- SQL: Ecto query syntax and parameterised `fragment("... ?", ^value)` are safe; `fragment` rejects string interpolation at compile time, but interpolating into a raw SQL string for `Ecto.Adapters.SQL.query` is injectable.
- Authorise from `conn.assigns.current_user`, not from user-supplied ids or emails; `cast/3` only the fields users may set (for example never `:is_admin` on a public signup).
- CORS: list exact origins (for example `["https://app.example.com"]`), never a broad regex such as `~r/^http.*/`.
- SSRF: do not build outbound URLs from user input; a client `base_url` (Req, Tesla) can be overridden by an absolute URL.
- The Phoenix guide points to the Erlang Ecosystem Foundation's web security best practices and secure coding and deployment hardening guidelines for more.

## Self-check
Submit a form POST without `_csrf_token` in a test and confirm the request is rejected with `InvalidCSRFTokenError`.

## Checked
2026-11-09. Rewritten from and confirmed against the Phoenix Security guide and the `Plug.CSRFProtection` module docs (Plug v1.20.3). Removed because those pages do not state them: the `Plug.Session` cookie options and `same_site`/`secure`/`http_only` values, `force_ssl: [hsts: true]`, `secret_key_base` handling (64 bytes, `mix phx.gen.secret`, rotation effects), password hashing libraries, `secure_compare`, rate-limiting library advice, and the 403 status.
Method: documentation only; no commands were run.
