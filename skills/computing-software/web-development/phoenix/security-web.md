---
id: computing-software.web-development.phoenix.security-web
name: security-web
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, security, xss, csrf, cors, access-control, mass-assignment, raw]
level: advanced
status: docs-checked
description: "Prevent XSS, CSRF, CORS misconfiguration and broken access control in Phoenix: raw/1, content types, protect_from_forgery, CORSPlug, cast."
sources:
  - https://hexdocs.pm/phoenix/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: avoid browser-facing and authorization vulnerabilities in Phoenix apps.

## XSS
Phoenix escapes output by default: `<%= "<hello>" %>` renders as escaped text, not a tag (angle brackets become HTML entities). `raw/1` bypasses this (`<%= raw "<b>hello</b>" %>` renders bold), so never pass user input to `raw/1`. Other vectors:
- building HTML from input: `html(conn, "<html><head>#{i}</head></html>")`
- `put_resp_content_type("text/html")` then `send_resp(200, "#{i}")`
- file uploads that serve the stored file with the user-supplied `content_type`: an uploaded `xss.html` containing `<html><script>alert(1)</script></html>` runs in the viewer's browser. Fix by restricting `put_resp_content_type` to image types only.

## CSRF
Browsers will send the session cookie on a cross-site form POST, so an attacker's page can submit a form to your site. Phoenix requires a random `_csrf_token` in forms, checked by `plug :protect_from_forgery` in the default `:browser` pipeline (alongside `:fetch_session`, `:put_secure_browser_headers`, etc.). Default settings are most likely safe.

Action re-use: never allow state-changing actions through GET. If the router maps both `get` and `post "/users/settings/edit_bio"` to the same `edit_bio` action, visiting `/users/settings/edit_bio?user%5Bbio%5D=Hacked+LOL` updates the bio with no token check. State changes (transfers, posts, account updates) go through POST with CSRF protection.

## CORS
Allow only trusted origins:
```elixir
plug CORSPlug, origin: ["https://app.example.com"]
```
A broad policy such as `plug CORSPlug, origin: ~r/^http.*/` lets any malicious site visited by a logged-in user read sensitive data such as API keys.

## Broken access control
Take the acting user from `conn.assigns.current_user`, not from request input. A common pattern:
```elixir
def action(conn, _) do
  args = [conn, conn.params, conn.assigns.current_user]
  apply(__MODULE__, action_name(conn), args)
end
```
Wrong: `def index(conn, %{"user" => user_email})` followed by `Accounts.get_user_by_email(user_email)`; an attacker just changes the email.

Mass assignment: Ecto forces you to list permitted fields in `cast/3`. Putting `:is_admin` in `cast(attrs, [:email, :password, :is_admin])` of a public registration changeset lets anyone create an admin; never cast privilege fields from external input.

Related: computing-software.web-development.phoenix.security-injection

## Checked

2026-11-08. Confirmed against the Phoenix guide source (phoenixframework/phoenix, guides/security.md, main branch, read in full), the published form of the cited hexdocs page: XSS, CSRF, action re-use CSRF, CORS and broken access control examples including mass assignment. Removed: nothing.

Method: documentation only; no commands were run.
