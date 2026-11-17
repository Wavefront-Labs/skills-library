---
id: computing-software.web-development.rails.rate-limiting-and-rack-attack
name: rate-limiting-and-rack-attack
category: computing-software
field: web-development
product: rails
tags: [rack-attack, rails-rate-limit, throttling, brute-force-protection, rails]
level: practitioner
status: docs-checked
description: "Rate limiting Rails apps: the built-in rate_limit controller macro, Rack::Attack throttles, blocklists and safelists, cache store requirements, and 429 responses."
sources:
  - https://api.rubyonrails.org/classes/ActionController/RateLimiting/ClassMethods.html
  - https://github.com/rack/rack-attack
  - https://guides.rubyonrails.org/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rate_limit and Rack::Attack

## 1. Built-in rate_limit
```ruby
class SessionsController < ApplicationController
  rate_limit to: 10, within: 3.minutes, only: :create, with: -> { redirect_to new_session_url, alert: "Try again later." }
end
class Api::SearchController < Api::BaseController
  rate_limit to: 100, within: 1.minute, by: -> { current_api_key.id }, name: "search"
end
```
- Default key is `request.remote_ip`; exceeding the limit raises `ActionController::TooManyRequests`, which Action Dispatch rescues as 429 Too Many Requests. `with:` customises the response, `scope:` shares a limit across controllers, and multiple limits per controller each need a `name:`.
- Backed by an `ActiveSupport::Cache` store: `config.action_controller.cache_store`, which defaults to the global `config.cache_store`, or pass `store:`. Use a store shared by all app processes (for example Redis) so counts are not per process.

## 2. Rack::Attack (middleware-level, app-wide)
```ruby
# config/initializers/rack_attack.rb
Rack::Attack.cache.store = ActiveSupport::Cache::RedisCacheStore.new(url: ENV["REDIS_URL"])

Rack::Attack.safelist("healthcheck") { |req| req.path == "/up" }
Rack::Attack.throttle("req/ip", limit: 300, period: 5.minutes) { |req| req.ip unless req.path.start_with?("/assets") }
Rack::Attack.throttle("logins/email", limit: 5, period: 20.seconds) do |req|
  req.params.dig("user", "email")&.downcase&.strip if req.path == "/session" && req.post?
end
Rack::Attack.blocklist("fail2ban scanners") do |req|
  Rack::Attack::Fail2Ban.filter("scan-#{req.ip}", maxretry: 3, findtime: 10.minutes, bantime: 1.hour) do
    req.path.include?("/wp-admin") || req.path.end_with?(".php")
  end
end
Rack::Attack.throttled_responder = lambda do |req|
  retry_after = (req.env["rack.attack.match_data"] || {})[:period]
  [429, { "Content-Type" => "application/json", "Retry-After" => retry_after.to_s }, [{ error: "rate_limited" }.to_json]]
end
```
Tell the app to use Rack::Attack as middleware (see the README). Safelists take precedence over blocklists and throttles; throttled requests get 429 by default. Throttle state lives in a configurable cache that defaults to `Rails.cache`; the README recommends a separate database for it.

## 3. Getting the IP right
Behind a load balancer make sure `req.ip` resolves to the real client, otherwise every user shares one bucket.

## 4. What to limit
Logins (per IP and per account), password reset, signup, OTP verification, expensive search/export endpoints, API keys per plan. Pair with account lockout alerts rather than permanent lockouts (which enable denial of service).

## Verify
- [ ] Limits enforced across multiple app processes (shared store); 429 with Retry-After returned; real client IPs used behind the proxy; health checks safelisted.

## Checked
2026-10-31. Confirmed against the Rails API page for ActionController::RateLimiting::ClassMethods (8.1.4) and the rack-attack README: rate_limit options (to, within, by, with, store, name, scope), remote_ip default, 429 via TooManyRequests, cache-store defaults, safelist precedence, Fail2Ban.filter maxretry/findtime/bantime, throttle limit/period, throttled_responder with rack.attack.match_data, 429 default, Rails.cache default. Removed: Rails 7.2 version gate, Rails 8 generator claim, memory-store claim, trusted_proxies and X-Forwarded-For specifics, middleware auto-insert claim.
Method: documentation only; no commands were run.
