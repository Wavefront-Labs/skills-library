---
id: computing-software.software-engineering.ruby.ruby-bundler-audit
name: ruby-bundler-audit
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, bundler-audit, supply-chain]
level: practitioner
status: docs-checked
description: "Scan Gemfile.lock for vulnerable gems with bundler-audit: update the advisory DB, ignore advisories, JSON output and Rake tasks."
sources: ["https://github.com/rubysec/bundler-audit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gem vulnerability auditing

`bundler-audit` provides patch-level verification for Bundler. It checks `Gemfile.lock` for vulnerable gem versions and for insecure gem sources (`http://` and `git://`), prints advisory information, and lets you ignore advisories that have been manually worked around.

```sh
gem install bundler-audit
bundle-audit                                  # audit Gemfile.lock
bundle-audit update                           # update the ruby-advisory-db
bundle-audit check --update                   # update the DB and check (useful for CI)
bundle-audit check --no-update                # check without updating the DB
bundle-audit check --ignore OSVDB-108664      # ignore a specific advisory
bundle-audit check --gemfile-lock Gemfile.custom.lock
bundle-audit check --format json --output bundle-audit.json
bundle-audit check --config bundler-audit.custom.yaml
```
Each finding shows Name, Version, Advisory, Criticality, URL, Title and a Solution listing the versions to update to; the run ends with "Unpatched versions found!" when there are findings.

Per-project ignores go in `.bundler-audit.yml`:
```yaml
---
ignore:
  - CVE-YYYY-XXXX
```
Rake tasks: `require 'bundler/audit/task'` then `Bundler::Audit::Task.new` adds `rake bundle:audit` and `rake bundle:audit:update`.

## Gotchas
- The tool needs git installed (the advisory DB is a git repository, ruby-advisory-db).
- The README says it does not require a network connection to run a check, but it also documents `update` to refresh the DB, which fetches from the network; run the update in CI or before an offline check.
- The README does not state exit codes or where the DB is stored; confirm the exit status in your pipeline before relying on it.

## Checked

Date: 2026-11-08. Read in full: the bundler-audit README on GitHub. Removed: the `bundle outdated` and `bundle update --conservative` commands and the Bundler man page source (page not read), exit status 1, DB location, the scheduling advice, the library lockfile advice and the scope limits (interpreter, native C libraries, JavaScript), none of which the README states.

Method: documentation only; no commands were run.
