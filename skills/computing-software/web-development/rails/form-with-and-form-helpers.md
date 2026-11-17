---
id: computing-software.web-development.rails.form-with-and-form-helpers
name: form-with-and-form-helpers
category: computing-software
field: web-development
product: rails
tags: [hotwire, action-view, form-with, form-helpers, fields-for, nested-attributes, rails-forms, turbo-forms]
level: practitioner
status: docs-checked
description: "Building Rails forms with form_with: model vs url forms, field helpers, nested attributes with fields_for, error display, and Turbo's 422 response requirement."
sources:
  - https://guides.rubyonrails.org/form_helpers.html
  - https://guides.rubyonrails.org/layouts_and_rendering.html
  - https://guides.rubyonrails.org/active_record_validations.html#customizing-error-field-wrapper
  - https://turbo.hotwired.dev/handbook/drive#redirecting-after-a-form-submission
  - https://api.rubyonrails.org/classes/ActionView/Helpers/FormHelper.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# form_with and form helpers

**Goal:** forms that map cleanly to models, show validation errors, and work with Turbo Drive.

## 1. Model-backed form
```erb
<%= form_with model: @project do |f| %>
  <% if @project.errors.any? %>
    <div id="error_explanation" role="alert"><ul><% @project.errors.full_messages.each do |m| %><li><%= m %></li><% end %></ul></div>
  <% end %>
  <%= f.label :name %>
  <%= f.text_field :name, required: true, aria: { invalid: @project.errors[:name].any? } %>
  <%= f.collection_select :owner_id, User.order(:name), :id, :name, prompt: "Choose an owner" %>
  <%= f.check_box :archived %> <%= f.label :archived %>
  <%= f.submit %>
<% end %>
```
- `model:` infers URL and method (POST for new, PATCH for persisted) and the param key (`project[name]`).
- `url:` + `scope:` for non-model forms (search, login): `form_with url: search_path, method: :get`.
- Forms are enhanced by Turbo Drive when Turbo is loaded; non-GET forms include a hidden `authenticity_token` input.

## 2. Controller pattern Turbo needs
```ruby
def create
  @project = Project.new(project_params)
  if @project.save then redirect_to @project, notice: "Created"
  else render :new, status: :unprocessable_entity end      # 422 so Turbo renders the errors
end
```
Per the Turbo handbook, after a stateful form submission Turbo Drive expects a redirect (it names HTTP 303) which it follows; the exception is a response with a 4xx or 5xx status, which is how validation errors are rendered (422 Unprocessable Content). The Rails guides write the failure render as `render :new, status: :unprocessable_entity`. Use `status: :see_other` on redirects after PATCH/DELETE so the follow-up request is a GET.

## 3. Nested attributes
```ruby
class Project < ApplicationRecord
  has_many :tasks, dependent: :destroy
  accepts_nested_attributes_for :tasks, allow_destroy: true, reject_if: :all_blank
end
# params.expect(project: [:name, tasks_attributes: [[:id, :title, :_destroy]]])   # or params.require(:project).permit(:name, tasks_attributes: [:id, :title, :_destroy])
```
```erb
<%= f.fields_for :tasks do |tf| %>
  <%= tf.text_field :title %> <%= tf.check_box :_destroy %>
<% end %>
```

## 4. Gotchas
- `check_box` emits a hidden `0` input before the checkbox so an unchecked box submits false.
- `collection_select` takes the value method first, then the text method: `f.collection_select :city_id, City.order(:name), :id, :name`.
- Fields with errors are wrapped in `<div class="field_with_errors">`; customise it with `config.action_view.field_error_proc`.

## Verify
- [ ] Invalid submit re-renders with errors (422) under Turbo; valid submit redirects.
- [ ] Nested rows add/remove/persist correctly; unpermitted params are reported according to `config.action_controller.action_on_unpermitted_parameters`.
- [ ] Labels associated (clicking label focuses input).

## Checked
Checked 2026-10-24 against the Rails 8.1.4 form helpers, layouts, validations and configuring guides and the Turbo handbook page on Drive (source markdown in hotwired/turbo-site). Confirmed: `form_with model:` and `url:` forms and param scoping, the hidden `authenticity_token`, hidden `0` field for checkboxes, `collection_select` argument order, `fields_for` with `accepts_nested_attributes_for` and `allow_destroy`/`_destroy`, `field_error_proc`, `render :new, status: :unprocessable_entity` in the guides, and the Turbo statements about redirects and 4xx/5xx responses. Removed the Rails 6.1/UJS comparison and the Stimulus template suggestion, which no checked page covers.

Method: documentation only; no commands were run.
