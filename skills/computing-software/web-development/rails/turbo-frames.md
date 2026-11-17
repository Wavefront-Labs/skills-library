---
id: computing-software.web-development.rails.turbo-frames
name: turbo-frames
category: computing-software
field: web-development
product: rails
tags: [hotwire, action-view, turbo-frames, turbo-frame, lazy-loading-frames, inline-editing, data-turbo-frame, turbo-rails]
level: practitioner
status: docs-checked
description: "Scoping navigation with Turbo Frames: inline edit, lazy-loaded frames, breaking out with target _top, frame-missing errors and when to use streams instead."
sources:
  - https://turbo.hotwired.dev/handbook/frames
  - https://turbo.hotwired.dev/reference/frames
  - https://github.com/hotwired/turbo-rails
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Turbo Frames

**Goal:** update just part of a page (inline edit, tabs, paginated panels, lazy sections) with plain server-rendered HTML.

## 1. Inline edit
```erb
<%# show / index %>
<%= turbo_frame_tag dom_id(project) do %>
  <h2><%= project.name %></h2>
  <%= link_to "Edit", edit_project_path(project) %>      <%# navigation stays inside the frame %>
<% end %>

<%# edit.html.erb - must contain a frame with the same id %>
<%= turbo_frame_tag dom_id(@project) do %>
  <%= render "form", project: @project %>
<% end %>
```
Turbo fetches the full edit page, extracts the matching `<turbo-frame id>`, and swaps it in. After `update` redirects to `show`, the frame from the show page replaces the form.

## 2. Lazy loading
```erb
<%= turbo_frame_tag "activity", src: project_activity_path(@project), loading: :lazy do %>
  <p>Loading activity…</p>
<% end %>
```
Loads when the frame becomes visible, like `loading="lazy"` on an `img`.

## 3. Targeting
- `data: { turbo_frame: "_top" }` on a link/form inside a frame -> full-page navigation (e.g. "View project" link inside a card).
- `turbo_frame_tag "x", target: "_top"` makes all its links break out.
- Link outside a frame can drive it: `data: { turbo_frame: "details" }`.
- `data-turbo-action="advance"` on a frame promotes frame navigations into browser history (URL updates).

## 4. Errors
If the response has no `<turbo-frame>` with the matching id (redirected to login, error page, or a page you forgot to wrap), Turbo cannot swap content in. Intercept `turbo:frame-missing` to transform the response or visit another location, or fix the template.

## 5. Frames vs streams
Frames: replace one region in response to navigation within it. Streams: update **several** regions or respond to actions/broadcasts (append a row, update a counter and flash together).

## Verify
- [ ] Edit/cancel/save cycle stays in the frame; history behaves as intended.
- [ ] Lazy frames load only when scrolled into view (network panel).
- [ ] Session expiry during a frame request results in a full-page login, not an empty frame.

## Checked

2026-10-28. Confirmed from the Turbo handbook and reference for frames (matching frame ids, `loading="lazy"`, `target="_top"` on a frame or `data-turbo-frame`, `data-turbo-action` promotes frame navigation to a visit, `turbo:frame-missing` event). Removed (not found): the `Turbo-Frame` request header and automatic slim layout claim, and the "Content missing" message.

Method: documentation only; no commands were run.
