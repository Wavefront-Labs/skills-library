---
id: computing-software.web-development.jekyll.publishing-a-theme
name: publishing-a-theme
category: computing-software
field: web-development
product: jekyll
tags: [publish-theme, rubygems, gem-build, gem-push, semantic-versioning]
level: practitioner
status: docs-checked
description: "Publish a Jekyll theme to RubyGems: git init and commit, gem build the gemspec, gem push, and release new versions with semantic version bumps."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Themes are published through RubyGems.org, which needs a (free) account.

1. Put the theme in a git repository:

   ```sh
   git init # Only the first time
   git add -A
   git commit -m "Init commit"
   ```

2. Package it, replacing `jekyll-theme-awesome` with your theme name:

   ```sh
   gem build jekyll-theme-awesome.gemspec
   ```

3. Push the packaged gem:

   ```sh
   gem push jekyll-theme-awesome-*.gem
   ```

4. For a new release, update the version number in the gemspec and repeat steps 1 to 3. Follow Semantic Versioning when bumping.

Before publishing make sure `/_site` is in `.gitignore`, so a locally previewed compiled site is not included when you distribute the theme. Gem-based theme updates reach users when they run `bundle update <THEME>`.

## Checked

2026-11-04. Confirmed against the Jekyll Themes page, publishing section: git steps, gem build, gem push, version bump with Semantic Versioning and the _site gitignore advice. Nothing removed.

Method: documentation only; no commands were run.
