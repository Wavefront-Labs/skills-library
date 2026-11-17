---
id: computing-software.web-development.rails.api-only-apps-and-json-rendering
name: api-only-apps-and-json-rendering
category: computing-software
field: web-development
product: rails
tags: [rails, rails-api, jbuilder, json-api, rack-cors, api-mode, serializers, ruby, web-development]
level: practitioner
status: docs-checked
description: "Building JSON APIs with Rails API mode: ActionController::API, Jbuilder views and caching, consistent error responses, token auth, CORS, versioning and pagination."
sources:
  - https://guides.rubyonrails.org/api_app.html
  - https://guides.rubyonrails.org/security.html
  - https://guides.rubyonrails.org/action_controller_advanced_topics.html
  - https://github.com/rails/jbuilder
  - https://github.com/cyu/rack-cors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API-only apps and JSON rendering

**Goal:** a lean Rails JSON API with explicit response shapes, predictable errors and secure cross-origin access.

## 1. API mode
```bash
rails new shop-api --api --database=postgresql
```
`--api` makes `ApplicationController` inherit from `ActionController::API` instead of `ActionController::Base` and starts the app with a more limited middleware stack (nothing primarily useful for browsers, such as cookies support). Add back only what you need; `bin/rails middleware` lists the stack. An existing full app can add `Api::BaseController < ActionController::API`.

## 2. Shape responses explicitly
Never `render json: @user` for models with sensitive columns - `as_json` dumps every attribute.
Jbuilder:
```ruby
# app/views/api/v1/orders/index.json.jbuilder
json.data do
  json.array! @orders, partial: "api/v1/orders/order", as: :order, cached: true
end
json.meta { json.page @page; json.pages @pages }
# _order.json.jbuilder
json.extract! order, :id, :status, :total_cents, :created_at
json.customer { json.extract! order.customer, :id, :name }
```
`cached: true` on collection partial rendering (Rails 6.0+) and `json.cache!` use fragment caching.

## 3. Errors in one format
```ruby
class Api::BaseController < ActionController::API
  rescue_from ActiveRecord::RecordNotFound do render json: { error: "not_found" }, status: :not_found end
  rescue_from ActionController::ParameterMissing do |e| render json: { error: "bad_request", detail: e.message }, status: :bad_request end
  private
  def render_invalid(record) = render(json: { error: "invalid", details: record.errors.to_hash }, status: :unprocessable_entity)
end
```

## 4. Params
```ruby
def order_params = params.expect(order: [:sku, :quantity])   # older style: params.require(:order).permit(:sku, :quantity)
```
`wrap_parameters` lets clients send `{ "sku": ... }` without the root key for JSON requests.

## 5. Auth
```ruby
include ActionController::HttpAuthentication::Token::ControllerMethods
before_action :authenticate
def authenticate
  authenticate_or_request_with_http_token do |token, _|
    @current_client = ApiToken.active.find_by(digest: Digest::SHA256.hexdigest(token))&.client
  end
end
```
`authenticate_or_request_with_http_token` comes from `ActionController::HttpAuthentication::Token::ControllerMethods`. Store token digests, not raw tokens.

## 6. CORS, versioning, pagination
```ruby
# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow { origins "https://app.example.com"; resource "/api/*", headers: :any, methods: %i[get post patch delete options], max_age: 600 }
end
```
Version in the path (`namespace :api { namespace :v1 }`), paginate every list (`meta` or `Link` headers), and rate limit with the built-in controller `rate_limit to: 100, within: 1.minute` (the security guide shows `rate_limit to: 10, within: 3.minutes, only: :create`).

## Verify
- [ ] Request specs assert exact JSON keys (no password_digest/tokens) using a schema matcher.
- [ ] 404/400/422 all return the same error envelope.
- [ ] CORS preflight from a non-allowed origin fails.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 API-app, security and Action Controller guides, the jbuilder README and the rack-cors README. Confirmed: `rails new --api`, `ActionController::API` and the reduced middleware stack, `params.expect`, `authenticate_or_request_with_http_token`, jbuilder `cached: true` and `json.cache!`, `Rack::Cors` inserted with `insert_before 0` and its `origins`/`resource`/`max_age` options, and the built-in `rate_limit` macro. Removed the unconfirmed `Rails 7.2+` version gate, the RFC 9457 suggestion, serializer-gem names, the pagy reference and the SPA/JWT opinion.

Method: documentation only; no commands were run.
