---
id: computing-software.web-development.jekyll.config-precedence-and-exclude-trap
name: config-precedence-and-exclude-trap
category: computing-software
field: web-development
product: jekyll
tags: [config-precedence, exclude-override, vendor-bundle, node-modules, invalid-date-error]
level: practitioner
status: docs-checked
description: "Resolve conflicting Jekyll settings (flags, config file, defaults) and avoid the exclude override that breaks builds with an invalid date error from vendor/bundle."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Precedence for conflicting settings, highest first:

1. Command-line flags
2. Configuration file settings
3. Defaults

From 3.3.0 Jekyll skips `node_modules` and certain `vendor` subdirectories by default. Defining your own `exclude:` array (Jekyll 3) overrides that default, and the build can fail with:

```
ERROR: YOUR SITE COULD NOT BE BUILT:
Invalid date '<%= Time.now.strftime('%Y-%m-%d %H:%M:%S %z') %>':
Document 'vendor/bundle/gems/jekyll-3.4.3/lib/site_template/_posts/0000-00-00-welcome-to-jekyll.markdown.erb'
does not have a valid date in front matter.
```

Adding only `vendor/bundle` fixes that, but other sub-directories under `/vendor/` (and `/node_modules/`) then get processed into `_site`. The proper fix is to include the defaults in your array. Up to 3.4.3:

```yaml
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor/bundle/
  - vendor/cache/
  - vendor/gems/
  - vendor/ruby/
  - any_additional_item # user-specific entries go at the end
```

From 3.5, `Gemfile` and `Gemfile.lock` are excluded by default too, so usually no `exclude` array is needed: modify, remove or comment out the existing one.

## Checked

2026-11-04. Confirmed against the Jekyll troubleshooting page (Configuration problems): the precedence order, the 3.3.0 note on `node_modules` and `vendor`, the invalid date error text, the `vendor/bundle` side effect, the default `exclude` list up to 3.4.3 and the 3.5 change. Removed a claim about Jekyll 4 adding user entries to the defaults, which the page does not state.

Method: documentation only; no commands were run.
