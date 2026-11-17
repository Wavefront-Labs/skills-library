---
id: computing-software.web-development.rails.instrumentation-and-error-reporting
name: instrumentation-and-error-reporting
category: computing-software
field: web-development
product: rails
tags: [active-support-notifications, rails-error-reporter, instrumentation, error-reporting, rails]
level: advanced
status: docs-checked
description: "Instrumenting Rails: ActiveSupport::Notifications subscribers, custom instrumentation, the Rails.error reporter with handle and record, and vendor subscribers."
sources:
  - https://guides.rubyonrails.org/active_support_instrumentation.html
  - https://guides.rubyonrails.org/error_reporting.html
  - https://guides.rubyonrails.org/8_1_release_notes.html
  - https://guides.rubyonrails.org/configuring.html#config-log-tags
  - https://api.rubyonrails.org/classes/ActiveSupport/ErrorReporter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumentation and error reporting

## 1. ActiveSupport::Notifications
Rails emits events for controllers, views, SQL, cache, jobs, mailers.
```ruby
# config/initializers/instrumentation.rb
ActiveSupport::Notifications.subscribe("sql.active_record") do |event|
  if event.duration > 200                       # event.duration is in milliseconds
    Rails.logger.warn("slow sql (#{event.duration.round(1)} ms): #{event.payload[:sql].truncate(500)}")
  end
end
ActiveSupport::Notifications.subscribe("process_action.action_controller") do |event|
  Rails.logger.info("#{event.payload[:controller]}##{event.payload[:action]} status=#{event.payload[:status]} db=#{event.payload[:db_runtime]}ms view=#{event.payload[:view_runtime]}ms")
end
```
Documented events include `process_action.action_controller` (payload keys such as `:controller`, `:action`, `:status`, `:view_runtime`, `:db_runtime`), `render_template.action_view`, `sql.active_record` (`:sql`, `:name`, `:binds`), `cache_read.active_support`, `perform.active_job`, `deliver.action_mailer` and `enqueue.active_job`. You can also subscribe with a regular expression, for example `/action_controller/`.

Custom:
```ruby
ActiveSupport::Notifications.instrument("charge.payments", amount: cents, provider: "stripe") { gateway.charge(...) }
```
Name custom events in the `event.library` format the guide describes (its example is `tweet.twitter`).

Rails 8.1 adds `Rails.event` for structured event reporting: `Rails.event.notify("user.signup", user_id: 123)`, `Rails.event.tagged("graphql") { ... }` and `Rails.event.set_context(request_id: "abc123")`; subscribers implement `#emit(event)`.

## 2. Rails.error
```ruby
Rails.error.handle(Stripe::APIError, fallback: -> { :unavailable }) { gateway.fetch_balance }   # report and swallow (severity :warning)
Rails.error.record { import_file(path) }                                                       # report and re-raise (handled: false, severity :error)
Rails.error.report(e, handled: true, severity: :warning, context: { order_id: order.id })
Rails.error.set_context(user_id: current_user&.id)                                             # per request
```
- Rails wraps HTTP requests, jobs and `rails runner` invocations in the error reporter, so unhandled errors are reported automatically (errors in `ActionDispatch::ExceptionWrapper.rescue_responses` are not reported for HTTP requests).
- A subscriber is any object with a `report(error, handled:, severity:, context:, source: nil)` method, registered once with `Rails.error.subscribe(MySubscriber.new)` (`unsubscribe` removes one). Some libraries, such as Sentry's and Honeybadger's, register a subscriber for you.
- `severity` is `:error`, `:warning` or `:info`; `source` defaults to `"application"`.
- `Rails.error.unexpected("should not happen")` reports and returns nil in production; in development and test the error is wrapped in a new error class and surfaced.

## 3. Logs and tracing
- `config.log_tags = [:request_id]` tags log lines with any method the request responds to, a Proc, or anything responding to `to_s`.

## Verify
- [ ] Slow SQL and request metrics emitted; handled errors reported with context via Rails.error; error vendor configured as a subscriber, not called directly throughout the code.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 instrumentation, error reporting, configuring and 8.1 release notes guides. Confirmed: `ActiveSupport::Notifications.subscribe` with an event argument (`event.duration` in ms), regex subscriptions, the listed event names and payload keys, the `event.library` naming convention, `Rails.error.handle/record/report/unexpected/set_context/subscribe`, severity and handled defaults, subscriber signature, automatic reporting for requests, jobs and runner, `Rails.event` in 8.1 and `config.log_tags`. Removed the SCHEMA-name filter, StatsD call, synchronous-subscriber remark, lograge and OpenTelemetry suggestions and the vendor list beyond Sentry and Honeybadger, which the checked pages do not support.

Method: documentation only; no commands were run.
