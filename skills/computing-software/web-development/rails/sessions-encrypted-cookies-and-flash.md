---
id: computing-software.web-development.rails.sessions-encrypted-cookies-and-flash
name: sessions-encrypted-cookies-and-flash
category: computing-software
field: web-development
product: rails
tags: [rails-flash, encrypted-cookies, rails-sessions, cookie-store, rails]
level: practitioner
status: docs-checked
description: "Rails sessions, cookies and flash: the encrypted cookie store and its limits, signed vs encrypted cookies, session security settings, flash vs flash.now, and flash with Turbo."
sources:
  - https://guides.rubyonrails.org/action_controller_overview.html#session
  - https://guides.rubyonrails.org/action_controller_overview.html#cookies
  - https://guides.rubyonrails.org/security.html#sessions
  - https://guides.rubyonrails.org/configuring.html#config-action-dispatch-cookies-same-site-protection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sessions, encrypted cookies and flash

## 1. Session store
Default `CookieStore` is the default and recommended store: all session data lives in the cookie, which uses the encrypted cookie jar (integrity and confidentiality), with keys derived from `secret_key_base`.
- 4 kB limit: store ids, not objects (`session[:user_id] = user.id`); the guide discourages storing model instances.
- Clients can't read or edit the cookie, but session cookies do not invalidate themselves and can be copied and replayed (the security guide's replay attack); keep data that must not be replayable (such as credits) in the database and only the user id in the session. Other stores: `CacheStore` (temporary) and `ActiveRecordStore` (the `activerecord-session_store` gem). The Rails 8 authentication generator stores a session id in a signed cookie and keeps a `Session` record in the database.
- Changing `secret_key_base` invalidates all existing sessions; configure `config.action_dispatch.cookies_rotations` to rotate them.

```ruby
Rails.application.config.session_store :cookie_store, key: "_your_app_session", domain: ".example.com"   # key = cookie name
```
Call `reset_session` after logging in to avoid session fixation (the guide recommends it); the default `SameSite` value is set by `config.action_dispatch.cookies_same_site_protection` (`:lax` with current defaults).

## 2. Cookies
```ruby
cookies[:theme] = { value: "dark", expires: 1.hour }          # a scalar value lasts until the browser closes
cookies.signed[:visitor_id] = id                              # readable by client, tamper-proof
cookies.encrypted[:prefs] = prefs.to_json                     # unreadable and tamper-proof
cookies.permanent[:locale] = "fr"                              # expires 20 years from now
cookies.permanent.encrypted[:remember_token] = token
cookies.delete(:theme)                                         # setting nil does not delete
```
The signed jar adds a signature, the encrypted jar also encrypts. The jars serialise values with `config.action_dispatch.cookies_serializer` (default `:json` for new apps), so `Date`, `Time` and `Symbol` come back as strings. `config.force_ssl = true` serves every request over HTTPS and adds the HSTS header.

## 3. Flash
```ruby
redirect_to @post, notice: "Saved"                  # flash[:notice] for the next request
flash[:alert] = "Not allowed"; redirect_to root_path
flash.now[:alert] = "Fix the errors below"          # current request only (with render)
render :edit, status: :unprocessable_entity
flash.keep                                           # carry over one more request
```
- Values set with plain `flash` are available on the next request; with `render` in the same request use `flash.now`, otherwise the message also shows on the next page.
- Any key works: `redirect_to root_url, flash: { just_signed_up: true }`. Display flash messages once in the application layout (`flash.each do |name, msg| ... end`).

## Verify
- [ ] Session reset after login; no flash duplicated after `render`; changing `secret_key_base` is planned with cookie rotations.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Action Controller overview, security and configuring guides. Confirmed: CookieStore as the default with 4 kB limit, encrypted cookie jar keyed from `secret_key_base`, replay risk, `CacheStore`/`ActiveRecordStore`, `key:` and `domain:` session options, `secret_key_base` change invalidating sessions and `cookies_rotations`, `reset_session` after login, signed/encrypted/permanent cookie jars and `cookies.delete`, `expires:`, JSON cookie serializer, `flash.keep`/`flash.now` and `flash:` hash, `force_ssl` with HSTS and the `:lax` SameSite default. Removed the AES-256-GCM claim, the `_app_session` default name, `secure:`/`same_site:`/`expire_after:` session options, the redis store gem, ARIA role advice and the Turbo Stream flash section, none of which the checked pages cover.

Method: documentation only; no commands were run.
