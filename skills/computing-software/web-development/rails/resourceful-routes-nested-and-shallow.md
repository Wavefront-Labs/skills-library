---
id: computing-software.web-development.rails.resourceful-routes-nested-and-shallow
name: resourceful-routes-nested-and-shallow
category: computing-software
field: web-development
product: rails
tags: [rails, resourceful-routes, nested-resources, shallow-nesting, routes-rb, rest, ruby, web-development, rails-routing]
level: practitioner
status: docs-checked
description: "Designing Rails routes: resources and resource, only/except, shallow nesting, member and collection routes, namespaces vs scopes, constraints and route debugging."
sources:
  - https://guides.rubyonrails.org/routing.html
  - https://api.rubyonrails.org/classes/ActionDispatch/Routing/Mapper/Resources.html
  - https://guides.rubyonrails.org/routing.html#shallow-nesting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resourceful routes, nesting and shallow routes

**Goal:** RESTful URLs with predictable helpers, no route sprawl.

## 1. Resources
```ruby
Rails.application.routes.draw do
  resources :projects, only: %i[index show new create edit update destroy]
  resource :profile, only: %i[show edit update]       # singular: no :id, current user's profile
  root "projects#index"
end
```
Seven actions: index, show, new, create, edit, update, destroy. Restrict with `only:` so nonexistent actions don't appear as routes.

## 2. New behaviour = new resource
Instead of `post :archive` everywhere, model it as a resource:
```ruby
resources :projects do
  resource :archive, only: %i[create destroy], module: :projects   # POST /projects/:project_id/archive -> Projects::ArchivesController#create
end
```
Use `member { post :duplicate }` / `collection { get :search }` sparingly.

## 3. Nesting and shallow
```ruby
resources :projects, shallow: true do
  resources :tasks           # index/new/create nested; show/edit/update/destroy at /tasks/:id
end
```
The guide's rule of thumb is to nest resources only 1 level deep. Shallow routes keep the collection actions (index, new, create) under the parent and give member actions (show, edit, update, destroy) short URLs; `shallow do ... end` makes every nesting inside a block shallow, and `shallow_path`/`shallow_prefix` on `scope` customise the paths and helpers. Helpers: `project_tasks_path(@project)`, `task_path(@task)`.

## 4. Namespaces vs scopes
```ruby
namespace :admin do resources :users end           # /admin/users -> Admin::UsersController, admin_users_path
scope module: :api do resources :orders end        # /orders -> Api::OrdersController
scope "/:locale", locale: /en|de/ do resources :pages end
namespace :api, defaults: { format: :json } do
  namespace :v1 do resources :orders, only: %i[index show] end
end
```

## 5. Constraints and concerns
```ruby
constraints subdomain: "app" do ... end
constraints ->(req) { AdminList.include?(req.remote_ip) } do resources :reports end   # an object with matches?(request), or a lambda, gets the request
mount MyRackApp, at: "/rack"                                                          # any object that responds to call
concern :commentable do resources :comments, only: %i[index create] end
resources :posts, concerns: :commentable
```
`direct(:homepage) { "https://example.com" }` for custom URL helpers.

## 6. Debugging
```bash
bin/rails routes -g task           # grep
bin/rails routes -c projects       # by controller
bin/rails routes --expanded
```
The router uses the first matching route, so put specific routes before `resources` lines that would capture them (`get "projects/export"` before `resources :projects`). `bin/rails routes --expanded` prints the expanded table.

## Verify
- [ ] `bin/rails routes` lists no unintended actions (only/except applied).
- [ ] No nesting deeper than one level.
- [ ] Mounted Rack apps and engines are behind authentication or a constraint.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 routing guide. Confirmed: the seven resourceful actions and `only:`, singular `resource`, `member`/`collection` blocks, `shallow: true` and `shallow do`, the 1-level nesting rule of thumb, `namespace` versus `scope module:`/`scope "/admin"`, optional `(:locale)` scopes, request-based constraints, `matches?` objects and lambdas, `concern`, `direct`, `defaults:`, Rack endpoints via `to:`/`mount`, first-match routing and the `bin/rails routes` `-g`, `-c` and `--expanded` options. Removed the Sidekiq and Mission Control mounts, which belong to other projects' docs.

Method: documentation only; no commands were run.
