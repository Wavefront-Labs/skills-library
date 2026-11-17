---
id: computing-software.web-development.rails.before-action-filters-and-concerns
name: before-action-filters-and-concerns
category: computing-software
field: web-development
product: rails
tags: [rails, before-action, rails-concerns, controller-filters, activesupport-concern, authorization, ruby, web-development, action-controller]
level: practitioner
status: docs-checked
description: "Structuring Rails controllers with before_action/around_action filters and concerns: ordering, only/except, skip_before_action pitfalls, and model concerns done well."
sources:
  - https://guides.rubyonrails.org/action_controller_overview.html#controller-callbacks
  - https://guides.rubyonrails.org/action_controller_advanced_topics.html
  - https://guides.rubyonrails.org/layouts_and_rendering.html
  - https://guides.rubyonrails.org/i18n.html
  - https://api.rubyonrails.org/classes/ActiveSupport/Concern.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# before_action filters and concerns

**Goal:** shared controller logic (auth, loading records, locale) declared once, with secure defaults.

## 1. Filters
```ruby
class ApplicationController < ActionController::Base
  before_action :require_authentication            # secure by default
  around_action :switch_locale
  private
  def switch_locale(&action)
    I18n.with_locale(params[:locale] || I18n.default_locale, &action)
  end
end

class ProjectsController < ApplicationController
  allow_unauthenticated_access only: %i[index show]   # Rails 8 auth generator helper; else skip_before_action
  before_action :set_project, only: %i[show edit update destroy]
  private
  def set_project
    @project = Current.user.projects.find(params[:id])    # scoped: other users' ids 404
  end
end
```
- A `before_action` that renders or redirects halts the request: the action and any later callbacks do not run. Callbacks defined in `ApplicationController` run for every controller. Registering the same callback again with different options overwrites the earlier registration.
- Record loaders: list actions with `only:`. Security filters: apply globally and opt out with `skip_before_action ..., only: [...]`, so new actions are protected by default.
- `skip_before_action :require_authentication` without `only:` disables auth for the whole controller - review every skip. `only:` and `except:` work on both registering and skipping.
- Callbacks can also be written as a block (`before_action { |controller| ... }`, which runs outside the controller's scope so private methods need `send`) or as a class responding to the callback method.

## 2. Controller concerns
```ruby
# app/controllers/concerns/paginatable.rb
module Paginatable
  extend ActiveSupport::Concern
  included do
    helper_method :page
  end
  private
  def page = [params.fetch(:page, 1).to_i, 1].max
end
```
`included do ... end` runs class-level macros (filters, `helper_method`, `rescue_from`) in the including class; `class_methods do ... end` defines class methods.

## 3. Model concerns
```ruby
module Archivable
  extend ActiveSupport::Concern
  included do
    scope :archived, -> { where.not(archived_at: nil) }
  end
  def archive! = update!(archived_at: Time.current)
end
```
Good concerns represent a role/trait (Archivable, Searchable) with cohesive behaviour. Bad ones are a dumping ground that splits a fat model into files without reducing complexity.

## 4. rescue_from
```ruby
rescue_from ActiveRecord::RecordNotFound, with: :record_not_found

private
  def record_not_found
    render file: "#{Rails.root}/public/404.html", status: :not_found, layout: false
  end
```

## Verify
- [ ] Every `skip_before_action :require_authentication` has an `only:` list and was reviewed.
- [ ] Record loaders scope through the current user/account.
- [ ] Request specs: unauthenticated access to each protected action redirects/401s.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Action Controller, advanced topics, layouts and i18n guides and the generated authentication concern. Confirmed: `before_action` halting on render/redirect, `skip_before_action` with `only:`, same-callback overwrite note, block and class callbacks, `around_action` with `I18n.with_locale`, `rescue_from ... with:`, `render file: "#{Rails.root}/public/404.html", layout: false`, and `allow_unauthenticated_access`, `class_methods`, `included do` and `helper_method` as used by the generator and engines guide. Removed the "parent class first" ordering claim, the "filters can't take arguments" claim and the Pundit example, which the checked pages do not support.

Method: documentation only; no commands were run.
