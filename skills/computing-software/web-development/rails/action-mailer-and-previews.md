---
id: computing-software.web-development.rails.action-mailer-and-previews
name: action-mailer-and-previews
category: computing-software
field: web-development
product: rails
tags: [rails, action-mailer, mailer-previews, deliver-later, email, interceptors, ruby, web-development]
level: practitioner
status: docs-checked
description: "Sending email with Rails Action Mailer: parameterised mailers, deliver_later, multipart templates, URL options, previews, interceptors for staging and tests."
sources:
  - https://guides.rubyonrails.org/action_mailer_basics.html
  - https://guides.rubyonrails.org/testing.html
  - https://github.com/rails/rails/blob/v8.1.4/actionmailer/lib/action_mailer/test_helper.rb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Action Mailer and previews

**Goal:** transactional emails that are sent asynchronously, render correctly, link to the right host, and are previewable and tested.

## 1. Mailer
```ruby
class OrderMailer < ApplicationMailer
  default from: email_address_with_name("orders@example.com", "Acme Orders")
  def confirmation
    @order = params[:order]
    attachments["invoice.pdf"] = @order.invoice_pdf if @order.invoice_pdf
    mail to: email_address_with_name(@order.email, @order.customer_name),
         subject: t(".subject", number: @order.number)
  end
end
OrderMailer.with(order: @order).confirmation.deliver_later   # enqueue via Active Job
```
- Templates: `app/views/order_mailer/confirmation.html.erb` and `.text.erb` -> multipart/alternative automatically. Always include text.
- Use `deliver_later` (job) from requests; `deliver_now` only inside jobs/scripts.
- Pass records via `with(...)`; Active Job serialises them by GlobalID - if the record is deleted before the job runs, the job raises `DeserializationError` (discard it in `ApplicationJob`).

## 2. URLs and assets
```ruby
config.action_mailer.default_url_options = { host: "example.com", protocol: "https" }
config.action_mailer.asset_host = "https://example.com"
```
Use `*_url` helpers (not `*_path`) in mailer views.

## 3. Delivery
```ruby
config.action_mailer.delivery_method = :smtp
config.action_mailer.smtp_settings = { address: "smtp.example.com", port: 587, user_name: Rails.application.credentials.dig(:smtp, :user_name), password: Rails.application.credentials.dig(:smtp, :password), authentication: "plain", enable_starttls: true }
```
Set `config.action_mailer.raise_delivery_errors = true` so delivery failures raise, and let the job retry.

## 4. Previews
```ruby
# test/mailers/previews/order_mailer_preview.rb
class OrderMailerPreview < ActionMailer::Preview
  def confirmation = OrderMailer.with(order: Order.last).confirmation
end
```
Visit `/rails/mailers` in development (a single preview is at `/rails/mailers/order_mailer/confirmation`); previews live in `test/mailers/previews` by default and `config.action_mailer.preview_paths` adds directories.

## 5. Staging safety
```ruby
class StagingInterceptor
  def self.delivering_email(message)
    message.to = ["qa@example.com"]
  end
end
# config/initializers/mail_interceptors.rb
Rails.application.configure do
  config.action_mailer.interceptors = %w[StagingInterceptor] if Rails.env.staging?
end
```
The guide shows this with a custom `staging` environment; a `before_deliver` callback in the mailer is the alternative.

## 6. Tests
```ruby
include ActionMailer::TestHelper
assert_enqueued_email_with OrderMailer, :confirmation, params: { order: order } do
  post orders_path, params: {...}
end
mail = OrderMailer.with(order:).confirmation
assert_equal ["buyer@example.com"], mail.to
assert_match order.number, mail.body.to_s
```

## Verify
- [ ] Every mailer has a preview and text part.
- [ ] Links in emails are absolute HTTPS URLs to the right host.
- [ ] Staging never emails real customers (interceptor or sandbox provider).

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Action Mailer and testing guides and the v8.1.4 test_helper source. Confirmed: `deliver_later` backed by Active Job, `with(...)` parameterised mailers, `email_address_with_name`, multipart/alternative from text and HTML templates, `default_url_options` and `asset_host`, the SMTP settings keys (`authentication: "plain"`, `enable_starttls`), `raise_delivery_errors`, `ActiveJob::DeserializationError` rescue, preview location and `/rails/mailers` URLs, interceptor registration through `config.action_mailer.interceptors`, and the `assert_enqueued_email_with` signature (`params:`). Removed premailer-rails, letter_opener, provider-gem and SPF/DKIM/DMARC advice and the FactoryBot fallback, which the checked pages do not cover.

Method: documentation only; no commands were run.
