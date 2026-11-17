---
id: computing-software.web-development.rails.rails-internationalisation-i18n
name: rails-internationalisation-i18n
category: computing-software
field: web-development
product: rails
tags: [rails-i18n, i18n, localisation, locale-files, rails]
level: practitioner
status: docs-checked
description: "Internationalising Rails apps: locale files and lazy lookup, locale per request, pluralisation, model and error translations, dates and numbers, i18n-tasks."
sources:
  - https://guides.rubyonrails.org/i18n.html
  - https://guides.rubyonrails.org/configuring.html#config-i18n-raise-on-missing-translations
  - https://github.com/svenfuchs/rails-i18n
  - https://github.com/glebm/i18n-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rails internationalisation (I18n)

## 1. Configuration
```ruby
# config/application.rb
config.i18n.available_locales = [:en, :de, :ja]
config.i18n.default_locale = :en
config.i18n.load_path += Dir[Rails.root.join("config/locales/**/*.{rb,yml}")]
config.i18n.raise_on_missing_translations = true   # defaults to false; the guide suggests enabling it in test (:strict also raises in models)
```
The `rails-i18n` gem provides locale data for many languages (including pluralization rules beyond English, which Rails applies only for English by default).

## 2. Setting the locale per request
```ruby
class ApplicationController < ActionController::Base
  around_action :switch_locale
  def switch_locale(&action)
    locale = params[:locale] || current_user&.locale || I18n.default_locale
    locale = I18n.default_locale unless I18n.available_locales.map(&:to_s).include?(locale.to_s)
    I18n.with_locale(locale, &action)            # applies for the block only, no leak between requests
  end
  def default_url_options = { locale: I18n.locale }
end
# routes.rb
scope "(:locale)", locale: /en|de|ja/ do
  resources :products
end
```
The guide warns that `I18n.locale = :es` in one request can affect other requests handled by the same thread/process; use `I18n.with_locale` (typically in an `around_action`). Always check the locale against `I18n.available_locales` before applying it. Link helpers keep the locale through `default_url_options`, whose result is cached per request.

## 3. Translations
```yaml
# config/locales/en.yml
en:
  products:
    index:
      title: "Products"
      count:
        zero: "No products"
        one: "1 product"
        other: "%{count} products"
  activerecord:
    models: { product: { one: "Product", other: "Products" } }
    attributes: { product: { price: "Price" } }
    errors:
      models: { product: { attributes: { price: { greater_than: "must be positive" } } } }
```
```erb
<h1><%= t(".title") %></h1>                    <%# lazy lookup: products.index.title %>
<%= t(".count", count: @products.size) %>
<%= t("welcome_html", name: link_to(user.name, user)) %>   <%# _html keys: interpolations are escaped, key marked safe %>
<%= l(order.created_at, format: :long) %>
<%= number_to_currency(price, locale: :de) %>
```
- By default only English pluralization rules apply; the rails-i18n gem supplies a fuller set of locale-specific rules.
- Don't concatenate translated fragments; translate whole sentences with interpolation.

## 4. Tooling
- The `i18n-tasks` gem: `bundle exec i18n-tasks health` reports missing and unused keys, `i18n-tasks unused` lists unused keys and `i18n-tasks normalize` normalises locale files; run them in CI.
- Keep keys semantic, not English text.

## Verify
- [ ] Missing translations raise in tests; locale switches via URL and persists for users; dates, numbers and errors localised; i18n-tasks clean in CI.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 I18n and configuring guides and the i18n-tasks README. Confirmed: `config.i18n.default_locale`, `load_path` and `available_locales` settings, `raise_on_missing_translations` default and `:strict`, `I18n.with_locale` in `around_action`, validating locale against `available_locales`, `default_url_options`, `scope "(:locale)"` routes, lazy lookup, `count:` pluralization, `_html` keys, `l` and `number_to_currency`, `activerecord.models/attributes` scopes, rails-i18n for pluralization rules, and the i18n-tasks `health`, `unused` and `normalize` commands. Removed the `http_accept_language` helper (not a Rails method), translation-service names and `i18n-js`, which no checked page covers.

Method: documentation only; no commands were run.
