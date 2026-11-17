---
id: computing-software.web-development.rails.authentication-generator-and-has-secure-password
name: authentication-generator-and-has-secure-password
category: computing-software
field: web-development
product: rails
tags: [rails, has-secure-password, rails-authentication, authentication-generator, sessions, password-reset, ruby, web-development]
level: practitioner
status: docs-checked
description: "Adding authentication in Rails 8 with the authentication generator and has_secure_password: sessions, Current, rate limiting, password resets with tokens and sign-up."
sources:
  - https://guides.rubyonrails.org/security.html#authentication
  - https://api.rubyonrails.org/classes/ActiveModel/SecurePassword/ClassMethods.html
  - https://github.com/rails/rails/blob/v8.1.4/railties/lib/rails/generators/rails/authentication/authentication_generator.rb
  - https://github.com/rails/rails/blob/v8.1.4/activerecord/lib/active_record/secure_password.rb
  - https://api.rubyonrails.org/classes/ActiveRecord/TokenFor/ClassMethods.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication generator and has_secure_password

**Goal:** secure, understandable session auth you own, without a heavyweight gem.

## 1. Generate (Rails 8)
```bash
bin/rails generate authentication
bin/rails db:migrate
```
Creates: `User` (`has_secure_password`, `has_many :sessions`, `normalizes :email_address`), `Session` model (user, ip_address, user_agent), `Current` (`Current.session`, `Current.user` delegated to the session), `Authentication` concern included in `ApplicationController`, `SessionsController`, `PasswordsController` + `PasswordsMailer` with views and a mailer preview, routes `resource :session` and `resources :passwords, param: :token`, and migrations for users (`email_address` unique, `password_digest`) and sessions. It enables the `bcrypt` gem in the Gemfile. Sign-up is **not** generated; wire up your own registration controller, views and routes.

## 2. How it works
- Login: `User.authenticate_by(params.permit(:email_address, :password))`; regardless of whether a record is found it hashes the password, which mitigates timing-based enumeration (Rails API docs).
- On success a `Session` row is created and its id stored in a signed, permanent, `httponly`, `same_site: :lax` cookie.
- `require_authentication` before_action is global; opt out with `allow_unauthenticated_access only: %i[new create]`.
- `SessionsController` has `rate_limit to: 10, within: 3.minutes, only: :create, with: -> { redirect_to new_session_path, alert: "Try again later." }`; `PasswordsController` has the same limit on `create`.
- Logout destroys the session row - server-side revocation, and you can list/kill sessions per user.

## 3. has_secure_password details
```ruby
class User < ApplicationRecord
  has_secure_password                      # adds password and password_confirmation, authenticate; validates presence on create, max 72 bytes, confirmation
  normalizes :email_address, with: ->(e) { e.strip.downcase }
  validates :password, length: { minimum: 12 }, allow_nil: true
end
```
Column `password_digest`. bcrypt handles at most 72 bytes - Rails validates the length. It does not validate minimum length or complexity; add that yourself. `has_secure_password :recovery_password` (with a `recovery_password_digest` column) supports an extra secret.

## 4. Password reset tokens
```ruby
generates_token_for :password_reset, expires_in: 15.minutes do
  password_salt.last(10)                    # token invalidates once the password changes
end
user.generate_token_for(:password_reset)
User.find_by_token_for(:password_reset, params[:token])
```
`has_secure_password` already provides `password_reset_token` and `find_by_password_reset_token(!)` built on `generates_token_for :password_reset` (15 minutes by default, configurable with `has_secure_password reset_token: { expires_in: 1.hour }`), using the last 10 characters of the password salt so the token stops working once the password changes. The generated `PasswordsController#create` responds the same whether or not the email exists.

## 5. Hardening checklist
- The generated `PasswordsController#update` runs `@user.sessions.destroy_all` after a reset; do the same on any password change.
- Add a minimum-length validation (`validates :password, length: { minimum: 12 }, allow_nil: true`).
- For email verification of sign-ups, `generates_token_for :email_verification` gives you the same expiring-token mechanism.

## 6. Scope
The generator covers password sessions and reset only; sign-up, email verification and any second factor are yours to add.

## Verify
- [ ] Wrong password and unknown email give the same response and similar timing.
- [ ] 11 rapid login attempts trigger the rate limit.
- [ ] Logging out on one device invalidates that session cookie server-side; reset tokens expire and are single-use after password change.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 security guide, the generator templates and the v8.1.4 secure_password sources. Confirmed: generated files, routes and migrations, bcrypt enablement, no sign-up flow, `authenticate_by` timing behaviour, cookie options (`signed.permanent`, `httponly`, `same_site: :lax`), `rate_limit to: 10, within: 3.minutes, only: :create`, `allow_unauthenticated_access`, 72-byte limit, reset token default of 15 minutes built on `generates_token_for` with the password salt, `sessions.destroy_all` on reset, and `has_secure_password :recovery_password`. Removed the MFA/passkey gem suggestions and the Devise comparison, which no checked page covers.

Method: documentation only; no commands were run.
