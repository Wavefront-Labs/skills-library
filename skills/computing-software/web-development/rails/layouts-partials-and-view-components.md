---
id: computing-software.web-development.rails.layouts-partials-and-view-components
name: layouts-partials-and-view-components
category: computing-software
field: web-development
product: rails
tags: [hotwire, action-view, rails-partials, view-components, layouts, content-for, collection-rendering, viewcomponent]
level: practitioner
status: docs-checked
description: "Structuring Rails views: layouts and content_for, partials with locals and strict locals, collection rendering with caching, and ViewComponent for testable UI."
sources:
  - https://guides.rubyonrails.org/layouts_and_rendering.html
  - https://guides.rubyonrails.org/action_view_overview.html#partials
  - https://viewcomponent.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layouts, partials and view components

**Goal:** views that are DRY, fast to render and testable, without a tangle of instance variables.

## 1. Layouts and content_for
```erb
<!-- app/views/layouts/application.html.erb -->
<title><%= content_for?(:title) ? "#{yield(:title)} - Acme" : "Acme" %></title>
<%= yield :head %>
<main id="main"><%= yield %></main>
<!-- in a view -->
<% content_for :title, @project.name %>
```
Per-controller layouts (`layout "admin"`) or nested layouts via `content_for` + `render template: "layouts/application"`.

## 2. Partials with explicit locals
```erb
<%= render "projects/card", project: @project, compact: true %>
```
```erb
<%# app/views/projects/_card.html.erb %>
<article class="card <%= 'card--compact' if compact %>"><h3><%= link_to project.name, project %></h3></article>
```
Pass what a partial needs as locals and don't read instance variables (`@project`) inside partials.

## 3. Collections
```erb
<%= render partial: "projects/card", collection: @projects, as: :project, cached: true %>
<%= render @projects %>    <%# shorthand, uses projects/_project.html.erb %>
```
Rendering a collection in one call replaces a per-item `render` loop; see the Action View guide for caching options.

## 4. ViewComponent
```ruby
class AvatarComponent < ViewComponent::Base
  def initialize(user:, size: 32) = (@user, @size = user, size)
  def render? = @user.present?
end
```
```erb
<%= render AvatarComponent.new(user: current_user) %>
```
Ruby objects with explicit inputs, unit-testable with `render_inline` (the ViewComponent site reports component unit tests much faster than controller tests). Good for a design system; partials remain fine for page fragments.

## 5. Helpers
Keep helpers small and pure (formatting); complex presentation logic -> components or presenters.

## Verify
- [ ] Shared partials take explicit locals; no instance variables inside partials.
- [ ] Component tests cover states (empty, long text, permissions).

## Checked
2026-10-28 Confirmed on the Rails guides (layouts_and_rendering: layout declarations; action_view_overview: partials, locals, collections) and the ViewComponent site (render_inline test helper; reports component unit tests over 100x faster than similar controller tests in the GitHub codebase). Removed: the strict-locals magic comment and Rails version claim, collection cache option and log line, Lookbook and Phlex mentions, the 'faster than partials' claim.
Method: documentation only; no commands were run.
