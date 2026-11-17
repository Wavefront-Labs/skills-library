---
id: computing-software.software-engineering.ruby.ruby-warning-deprecations
name: ruby-warning-deprecations
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, warning-deprecations, upgrades]
level: practitioner
status: docs-checked
description: "Surface and handle Ruby deprecation warnings with -W, Warning[:deprecated], Warning.warn hooks and CI gating before upgrades."
sources: ["https://docs.ruby-lang.org/en/master/Warning.html", "https://docs.ruby-lang.org/en/master/Kernel.html#method-i-warn"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warnings and deprecations

Deprecation warnings are off by default (`Warning[:deprecated]` is false). Turn them on to prepare an upgrade:
```sh
ruby -W:deprecated script.rb    # enable one category
RUBYOPT="-W:deprecated" bundle exec rspec
ruby -W:no-experimental x.rb    # silence a category
```
`-w` is a synonym for `-W1`; `-W0` is silent. In code:
```ruby
Warning[:deprecated] = true     # categories: :deprecated, :experimental, :performance
Warning[:performance] = true    # performance warnings, added in Ruby 3.3
def old_api
  warn "old_api is deprecated, use new_api", uplevel: 1, category: :deprecated
end
module CiWarnings               # hook: fail the build or route to a logger
  def warn(message, category: nil, **kwargs)
    raise message if category == :deprecated && ENV["CI"]
    super
  end
end
Warning.extend(CiWarnings)      # the documented way; keep `super` for default behaviour
```
`uplevel: 1` prefixes the caller's file and line, which makes the warning actionable. `Warning.warn` is called for all warnings Ruby issues, so a hook can filter by matching `message`. Never redefine the `Warning#warn` instance method itself.

## Gotchas
- Warnings print to `$stderr` by default and are easy to miss in test runners or daemons; capture them in CI logs.
- `Kernel#warn` does nothing when warnings are disabled (for example `-W0`).
- `-W:no-<category>` suppresses a category; `Warning[:experimental]` is true by default while `:deprecated` and `:performance` are false.

Verify: define `old_api`, call it with `RUBYOPT=-W:deprecated` (or `Warning[:deprecated] = true`), and confirm the message names the calling line.

## Checked
2026-11-03. Confirmed against ruby/ruby `warning.rb` (`Kernel#warn`, uplevel, categories), `error.c` (Warning module and the `Warning.extend` hook pattern), `doc/language/options.md` (`-w`, `-W`, `-W:no-category`, category defaults), `ruby.c` (`-W[level=2|:category]`, RUBYOPT) and `doc/NEWS/NEWS-3.3.0.md` (`Warning[:performance]`). Removed: the Ruby 2.7.2 default-change date, the claim that `-w` includes deprecated, keyword-argument migration advice, `$VERBOSE = nil` and once-per-call-site claims. The old hook redefined `Warning.warn` directly; replaced with the documented extend pattern.
Method: documentation only; no commands were run.
