---
id: computing-software.web-development.rails.routing-constraints-namespaces-and-concerns
name: routing-constraints-namespaces-and-concerns
category: computing-software
field: web-development
product: rails
tags: [routing-constraints, route-concerns, rails-namespaces, scope-module, rails]
level: practitioner
status: docs-checked
description: "Organising Rails routes: namespace vs scope vs module, routing concerns, segment, request and lambda constraints, subdomains, and inspecting with rails routes."
sources:
  - https://guides.rubyonrails.org/routing.html
  - https://api.rubyonrails.org/classes/ActionDispatch/Routing/Mapper/Concerns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Routing constraints, namespaces and concerns

## 1. namespace, scope, module
```ruby
namespace :admin do            # URL /admin/users, controller Admin::UsersController, helper admin_users_path
  resources :users
end
scope module: :admin do        # URL /users, controller Admin::UsersController
  resources :reports
end
scope "/v1", as: "v1" do       # URL /v1/orders, controller OrdersController, helper v1_orders_path
  resources :orders
end
```

## 2. Concerns
```ruby
concern :commentable do
  resources :comments, only: [:index, :create]
end
concern :archivable do
  member { patch :archive; patch :unarchive }
end
resources :posts, concerns: [:commentable, :archivable]
resources :photos, concerns: :commentable
```
Keeps shared nested routes consistent across resources.

## 3. Constraints
```ruby
get "photos/:id", to: "photos#show", constraints: { id: /\d+/ }        # segment constraint
get "posts/:slug", to: "posts#show", constraints: { slug: /[a-z0-9-]+/ }
constraints subdomain: "api" do
  scope module: :api, defaults: { format: :json } do
    resources :orders
  end
end
constraints(->(req) { RestrictedList.retrieve_ips.include?(req.remote_ip) }) do   # lambda, as in the guide
  get "*path", to: "restricted_list#index"
end
```
- Constraint classes: any object responding to `matches?(request)`; a lambda also receives the request.
- Anything mounted as a Rack app or engine (`mount MyEngine => "/path"`) that must not be public needs its own authentication or a constraint like the above.
- `:constraints` regexes cannot use anchors (`^`, `$`); the guide notes that all routes are anchored at the start and end already.

## 4. Other routing tools
- `direct(:homepage) { "https://example.com" }` and `resolve("Basket") { [:basket] }` for custom URL helpers.
- `draw(:admin)` loads `config/routes/admin.rb` to split large route files.
- `shallow: true` for deeply nested resources.

## 5. Inspect
`bin/rails routes -g admin` (grep), `-c Admin::Users` (controller), `--expanded`; `/rails/info/routes` in development.

## Verify
- [ ] Route listing shows expected helpers and controllers; constraint-protected mounts return 404 for non-admins; invalid ids don't reach controllers.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 routing guide. Confirmed: `namespace` versus `scope module:` and `scope "/path", as:` behaviour, `concern` with `concerns:` (single or array), segment constraints, request-based `subdomain:` constraints, `matches?` objects and lambdas, the no-anchors rule, `direct`, `resolve`, `draw(:admin)` loading `config/routes/admin.rb`, `shallow: true`, and `bin/rails routes -g/-c/--expanded` plus `/rails/info/routes`. Removed the Sidekiq, Mission Control, Flipper and Devise/warden examples, which belong to other projects' documentation.

Method: documentation only; no commands were run.
