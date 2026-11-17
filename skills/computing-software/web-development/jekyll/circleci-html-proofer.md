---
id: computing-software.web-development.jekyll.circleci-html-proofer
name: circleci-html-proofer
category: computing-software
field: web-development
product: jekyll
tags: [circleci, html-proofer, ci-testing, s3-deploy, gemfile-lock, gem-caching]
level: advanced
status: docs-checked
description: "Build, test and deploy Jekyll on CircleCI: Gemfile with html-proofer, jekyll build, htmlproofer flags, gem caching, workspace handoff and an S3 sync deploy job."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/continuous-integration/circleci.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Follow the project from CircleCI's Add Projects page (GitHub or Bitbucket), then add `.circleci/config.yml` at the repository root.

Dependencies come from a `Gemfile` listing Jekyll, plugins and HTML Proofer; commit `Gemfile.lock` too:

```ruby
source 'https://rubygems.org'
gem "jekyll"
gem "html-proofer"
```

Tests: first `bundle exec jekyll build` (a blocker for later tests), then HTML Proofer for valid HTML and broken links:

```sh
bundle exec htmlproofer ./_site --check-html --disable-external
```

See the html-proofer README or `htmlproofer --help` for all flags.

Complete config shape: workflow `test-deploy` with `build` then `deploy` (requires `build`, only on `master`). The build job uses a Ruby docker image with `BUNDLE_PATH: ~/repo/vendor/bundle`, restores a cache keyed on the `Gemfile.lock` checksum, runs `bundle check || bundle install`, saves the cache, builds, runs htmlproofer, and persists `_site` to the workspace. The deploy job attaches the workspace, installs the AWS CLI and runs:

```sh
~/.local/bin/aws s3 sync ./_site s3://$S3_BUCKET_NAME/ --delete --acl public-read
```

Set the `S3_BUCKET_NAME` environment variable in CircleCI first.

## Checked

2026-11-04. Confirmed against the Jekyll CircleCI continuous-integration page: Gemfile, htmlproofer flags, cache and workspace job shape, S3 sync command and S3_BUCKET_NAME. Nothing removed.

Method: documentation only; no commands were run.
