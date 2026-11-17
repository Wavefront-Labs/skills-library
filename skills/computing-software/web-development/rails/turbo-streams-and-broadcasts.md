---
id: computing-software.web-development.rails.turbo-streams-and-broadcasts
name: turbo-streams-and-broadcasts
category: computing-software
field: web-development
product: rails
tags: [hotwire, action-view, turbo-streams, turbo-stream-broadcast, broadcasts-to, turbo-stream-actions, morphing, real-time-updates]
level: practitioner
status: docs-checked
description: "Updating multiple page regions with Turbo Streams: stream actions from form responses, model broadcasts over Action Cable, morph refreshes and authorization of streams."
sources:
  - https://turbo.hotwired.dev/handbook/streams
  - https://github.com/hotwired/turbo-rails
  - https://turbo.hotwired.dev/handbook/page_refreshes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Turbo Streams and broadcasts

**Goal:** after an action (or another user's action), the right parts of the page update without writing JavaScript.

## 1. Stream response to a form
```ruby
def create
  @task = @project.tasks.create!(task_params)
  respond_to do |format|
    format.turbo_stream            # renders create.turbo_stream.erb
    format.html { redirect_to @project }
  end
end
```
```erb
<%# create.turbo_stream.erb %>
<%= turbo_stream.append "tasks", @task %>                       <%# renders tasks/_task partial %>
<%= turbo_stream.update "task_count", @project.tasks.count %>
<%= turbo_stream.replace "new_task", partial: "tasks/form", locals: { task: Task.new } %>
```
Actions are listed in the Turbo Streams handbook (the code above uses `append`, `update` and `replace`). Use `target` (a DOM id) for one element, or `targets` with a CSS query selector for several.

## 2. Broadcasts (real time)
```erb
<%= turbo_stream_from @project %>      <%# subscribes via Action Cable %>
```
```ruby
class Project < ApplicationRecord
  broadcasts_refreshes      # broadcasts a page refresh to subscribers of this record's stream
end
```
- turbo-rails delivers updates with asynchronous partial rendering and Action Cable (README).
- With refresh broadcasts each client re-fetches the page, so per-user content stays per-user.
- For sensitive streams, scope stream names per user or tenant.

## 3. Page refresh with morphing
`<meta name="turbo-refresh-method" content="morph">` + `turbo-refresh-scroll="preserve"`: redirects back to the same page and broadcast refreshes morph the DOM with scroll preserved - often simpler than hand-written stream templates. Mark islands to keep with `data-turbo-permanent`.

## Verify
- [ ] Creating a task updates list, counter and form in one response.
- [ ] Second browser sees changes live; per-user content isn't leaked through broadcasts.
- [ ] HTML format fallback works without JS.

## Checked

2026-10-28. Confirmed from the Turbo handbook (streams: `targets` with a CSS query selector; page refreshes: `turbo-refresh-method`, `turbo-refresh-scroll`, `data-turbo-permanent`, `broadcasts_refreshes` with `turbo_stream_from`) and the turbo-rails README (`turbo_stream_from`, asynchronous partial rendering over Action Cable). Removed (not found): the full action list including `refresh`/`morph`, `broadcasts_to`, `_later` variants, signed stream names, Rails 7.1 note, `current_user` behaviour, the Turbo 8 label and focus preservation.

Method: documentation only; no commands were run.
