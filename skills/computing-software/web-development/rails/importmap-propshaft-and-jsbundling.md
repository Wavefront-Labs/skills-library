---
id: computing-software.web-development.rails.importmap-propshaft-and-jsbundling
name: importmap-propshaft-and-jsbundling
category: computing-software
field: web-development
product: rails
tags: [hotwire, action-view, importmap-rails, propshaft, jsbundling-rails, cssbundling-rails, asset-pipeline, sprockets-migration, rails-assets]
level: practitioner
status: docs-checked
description: "Choosing and running the Rails asset stack: importmap-rails with Propshaft (no Node), jsbundling/cssbundling with esbuild or Bun, pinning packages and Sprockets migration."
sources:
  - https://github.com/rails/importmap-rails
  - https://github.com/rails/propshaft
  - https://github.com/rails/jsbundling-rails
  - https://github.com/rails/tailwindcss-rails
  - https://guides.rubyonrails.org/8_0_release_notes.html
  - https://guides.rubyonrails.org/asset_pipeline.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importmap, Propshaft and jsbundling

**Goal:** a working, fingerprinted asset setup that matches how much JavaScript the app actually has.

## 1. Pick the stack
| Situation | Stack |
|---|---|
| Hotwire app, modest JS, no JSX/TS | **importmap-rails + Propshaft** (importmap-rails is included for new apps from Rails 7; Propshaft is the default asset pipeline in Rails 8.0) - no Node, no build step |
| Need a Node-based bundler (TypeScript/JSX/React, packages that need bundling) | **jsbundling-rails** (Bun, esbuild, rollup.js or Webpack) + Propshaft |
| Tailwind | `tailwindcss-rails` (depends on `tailwindcss-ruby` for a Tailwind CLI executable) or `cssbundling-rails` |
| Legacy app | Sprockets; the Propshaft README says migrating can be a fair bit of work if you rely on Sprockets transpiling |

## 2. importmap-rails
```bash
bin/importmap pin chart.js           # downloads to vendor/javascript and adds a pin (JSPM by default; --from unpkg or jsdelivr)
bin/importmap outdated               # checks the npm registry for new versions
bin/importmap audit                  # checks the npm registry for known security issues
```
```ruby
# config/importmap.rb
pin "application"
pin_all_from "app/javascript/controllers", under: "controllers"
pin "chart.js", to: "chart.js"       # vendored file
```
`<%= javascript_importmap_tags %>` inlines the import map in the `<head>` (a `<script type="importmap">` tag), emits modulepreload links (controlled per pin with `preload:`) and loads the entry module. Local files under `app/javascript` must be pinned (for example with `pin_all_from`) when using Propshaft. Packages that need a build step are not a fit for importmaps; use jsbundling.

## 3. Propshaft
Copies all assets from the paths in `config.assets.paths` into `public/assets` when precompiling, stamping each with a digest; converts asset references in CSS (`url(...)`) to digested names. It is not a transpiler or bundler. Run `bin/rails assets:precompile` in deploy; `config.assets.excluded_paths` exempts directories that are only inputs.

## 4. jsbundling
`./bin/dev` starts the Rails server and the JS build watcher; the bundler writes `app/javascript/application.js` to `app/assets/builds/application.js`, which the asset pipeline serves. In production the `javascript:build` task attaches to `assets:precompile` so package dependencies are installed and bundled. The build image needs the bundler's runtime (Bun must already be installed if you use it).

## 5. Migration from Sprockets
Propshaft does less than Sprockets by design: stop transpiling (CoffeeScript, Sass) or move it to a Node-based tool such as jsbundling-rails and cssbundling-rails; if you already bundle through Node, Propshaft only digests and serves.

## Verify
- [ ] Production HTML references digested asset URLs.
- [ ] `bin/importmap audit` / `npm audit` clean or triaged.
- [ ] Fresh clone: `bin/setup && bin/dev` works without manual steps.

## Checked
Checked 2026-10-24 against the README files of importmap-rails, propshaft, jsbundling-rails and tailwindcss-rails (default branches) and the Rails 8.0 release notes. Confirmed: importmap included for new apps from Rails 7, Propshaft default in 8.0, `bin/importmap pin/outdated/audit`, vendoring to `vendor/javascript`, `pin_all_from`, `javascript_importmap_tags`, `preload:`, Propshaft copying, digesting and CSS `url()` rewriting, `config.assets.excluded_paths`, jsbundling output to `app/assets/builds` with `javascript:build` attached to `assets:precompile` and `bin/dev`, and tailwindcss-rails depending on `tailwindcss-ruby`. Removed the Rails 7.1 vendoring gate, the `bin/importmap update` command, the HTTP/2 and long-cache-header remarks and the tree-shaking claim, none of which the READMEs state.

Method: documentation only; no commands were run.
