---
id: computing-software.web-development.rails.respond-to-formats-rendering-and-redirects
name: respond-to-formats-rendering-and-redirects
category: computing-software
field: web-development
product: rails
tags: [respond-to, rails-rendering, redirect-to, turbo-stream-format, rails]
level: practitioner
status: docs-checked
description: "Rails controller responses: respond_to for HTML, JSON and Turbo Stream, render vs redirect_to, status codes for Turbo forms (422, 303), head responses, and avoiding double render."
sources:
  - https://guides.rubyonrails.org/layouts_and_rendering.html
  - https://guides.rubyonrails.org/action_controller_overview.html
  - https://guides.rubyonrails.org/configuring.html#config-action-controller-action-on-open-redirect
  - https://turbo.hotwired.dev/handbook/drive#redirecting-after-a-form-submission
  - https://turbo.hotwired.dev/handbook/streams#streaming-from-http-responses
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# respond_to, rendering and redirects

## 1. Formats
```ruby
def create
  @comment = @post.comments.build(comment_params)
  respond_to do |format|
    if @comment.save
      format.turbo_stream                                         # renders create.turbo_stream.erb
      format.html { redirect_to @post, notice: "Comment added" }
      format.json { render :show, status: :created, location: @comment }
    else
      format.html { render :new, status: :unprocessable_entity }   # 422
      format.json { render json: @comment.errors, status: :unprocessable_entity }
    end
  end
end
```
- An unsupported format raises `ActionController::UnknownFormat`, which Rails maps to 406 (`:not_acceptable`).
- For `POST`, `PUT`, `PATCH` and `DELETE` form submissions Turbo adds `text/vnd.turbo-stream.html` to the `Accept` header (it does not for links or `GET` forms by default), which is what makes `format.turbo_stream` match.

## 2. Status codes Turbo needs
- Failed validation: render with **422** (`render :new, status: :unprocessable_entity`, as the Rails guides write it). The Turbo handbook says that after a form submission Turbo Drive expects a redirect, except when the response has a 4xx or 5xx status, which is how validation errors (422) and server errors (500) are displayed.
- After success: redirect (`redirect_to` sends 302 by default; the Turbo handbook names HTTP 303). Use `status: :see_other` (303) for redirects after `DELETE`/`PATCH` so the follow-up request is a GET.

## 3. render vs redirect_to
- `render :edit` reuses instance variables and shows errors; URL stays the same.
- `redirect_to path` starts a new request (post/redirect/get) - use after successful writes so refresh doesn't resubmit.
- `redirect_back_or_to root_path` (the guide shows `redirect_back(fallback_location: root_path)`, which returns to the previous page) for "return where you came from"; `redirect_to url, allow_other_host: true` only for vetted external URLs: with `config.load_defaults 7.0` or later an external-host redirect raises `ActionController::Redirecting::UnsafeRedirectError` (`config.action_controller.action_on_open_redirect` defaults to `:raise` from 7.0, `:log` before).

## 4. Other responses
```ruby
head :no_content                                     # 204 for APIs/JS calls
render plain: "OK"; render json: { ok: true }; render html: helpers.tag.strong("Not Found")
render partial: "comments/comment", collection: @comments, cached: true   # collection caching, see the caching guide
send_data csv, filename: "orders.csv", type: "text/csv"
```

## 5. Double render
Calling `render`/`redirect_to` twice in an action raises the error "Can only render or redirect once per action". `redirect_to` and `redirect_back` do not halt the method, so add an explicit `return` after an early render or redirect inside a conditional. A `before_action` that renders or redirects halts the chain.

## Verify
- [ ] Invalid forms return 422 and re-render with errors under Turbo; successful writes redirect; JSON clients get correct status codes and Location headers.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 layouts and rendering, caching and configuring guides, the v8.1.4 redirecting source and the Turbo handbook (Drive and Streams pages, source markdown in hotwired/turbo-site). Confirmed: `respond_to` blocks, 302 default for `redirect_to` and `status:` override, 303/`:see_other`, `head`, `render plain/json/html`, `send_data`, the double-render error and explicit `return`, `redirect_back`/`redirect_back_or_to`, `allow_other_host: true` with `UnsafeRedirectError`, `UnknownFormat` mapped to 406, collection `cached:` rendering, and Turbo's Accept header and 4xx/5xx behaviour. Removed the `:unprocessable_content` Rack 3.1 note, the claim that Turbo "ignores" 200 form responses (the handbook states the redirect expectation instead) and the `.html_safe` render example.

Method: documentation only; no commands were run.
