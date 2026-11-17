---
id: computing-software.web-development.rails.rescue-from-and-error-pages
name: rescue-from-and-error-pages
category: computing-software
field: web-development
product: rails
tags: [rescue-from, rails-error-pages, exceptions-app, record-not-found, error-handling, rails]
level: practitioner
status: docs-checked
description: "Handling exceptions in Rails controllers: rescue_from order and scope, JSON vs HTML responses, default status mappings, custom error pages with exceptions_app, and reporting."
sources:
  - https://guides.rubyonrails.org/action_controller_advanced_topics.html#handling-errors
  - https://guides.rubyonrails.org/configuring.html#config-action-dispatch-rescue-responses
  - https://guides.rubyonrails.org/configuring.html#config-action-dispatch-show-exceptions
  - https://guides.rubyonrails.org/configuring.html#config-exceptions-app
  - https://guides.rubyonrails.org/error_reporting.html
  - https://github.com/rails/rails/blob/v8.1.4/actionpack/lib/action_dispatch/middleware/show_exceptions.rb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rescue_from and error pages

## 1. Default mappings
Rails already maps common exceptions to statuses (`config.action_dispatch.rescue_responses`, observable through `ActionDispatch::ExceptionWrapper.rescue_responses`): `ActiveRecord::RecordNotFound` -> 404, `ActionController::ParameterMissing` -> 400, `ActionController::InvalidAuthenticityToken` -> 422, `ActiveRecord::RecordInvalid` -> 422, `ActionController::RoutingError` -> 404; anything not configured becomes 500. Add your own with `config.action_dispatch.rescue_responses["MyAuthenticationError"] = :unauthorized`. You only need `rescue_from` for custom behaviour.

## 2. rescue_from
```ruby
class ApplicationController < ActionController::Base
  rescue_from StandardError, with: :internal_error if Rails.env.production?   # broadest first
  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from User::NotAuthorized, with: :forbidden                          # your own exception class

  private
  def not_found = respond_error(:not_found, "Not found")
  def forbidden = respond_error(:forbidden, "You are not allowed to do that")
  def internal_error(e)
    Rails.error.report(e, handled: true)
    respond_error(:internal_server_error, "Something went wrong")
  end
  def respond_error(status, message)
    respond_to do |f|
      f.html { render "errors/show", status:, locals: { message: }, layout: "application" }
      f.json { render json: { error: message }, status: }
      f.any  { head status }
    end
  end
end
```
Handlers are searched from the **last declared** upward (Active Support's `Rescuable` reads the handler list in reverse), so declare general ones first and specific ones after. The guide warns that `rescue_from` with `Exception` or `StandardError` has serious side effects because it stops Rails handling exceptions properly, so keep a strong reason for it; a handler can be a method, a `Proc` or a block, and some exceptions are only rescuable from `ApplicationController` because they are raised before the controller is initialized.

## 3. Custom error pages for everything else
In production Rails renders static files from `public/` (`404.html`, `500.html` and so on; they are plain HTML, so no ERB, SCSS or layouts), and a blocked browser gets `public/406-unsupported-browser.html`. `config.exceptions_app` (default `ActionDispatch::PublicExceptions.new(Rails.public_path)`) is the Rack app that `ShowExceptions` calls with `PATH_INFO` rewritten to the status code, so routes can render dynamic pages with your layout:
```ruby
# config/application.rb
config.exceptions_app = routes
# routes.rb
match "/404", to: "errors#not_found", via: :all
match "/500", to: "errors#internal", via: :all
```
Keep the 500 page dependency-free (no DB calls) so it renders even when the DB is down.

## 4. Development and tests
`config.action_dispatch.show_exceptions` controls how exceptions raised while responding are handled: `:all` renders error pages for all exceptions, `:rescuable` only for those in `rescue_responses` (and raises the rest), `:none` raises everything. The default has been `:all` since 7.1 (it was `true` before).

## Verify
- [ ] Missing record returns a 404 page (HTML) and `{"error":"Not found"}` (JSON); unhandled errors reach the error tracker with request context.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Action Controller advanced topics, configuring and error reporting guides and the v8.1.4 ShowExceptions and Rescuable sources. Confirmed: the default `rescue_responses` mapping (404/400/422 and 500 for unmapped), `rescue_from` handler forms and the Exception/StandardError warning, reverse handler search order, static `public/*.html` pages, `406-unsupported-browser.html`, `config.exceptions_app` default and PATH_INFO rewrite, and the `show_exceptions` values and 7.1 default. Removed the Pundit example and the `400.html` claim, which the checked pages do not support.

Method: documentation only; no commands were run.
