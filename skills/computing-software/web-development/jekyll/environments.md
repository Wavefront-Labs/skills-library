---
id: computing-software.web-development.jekyll.environments
name: environments
category: computing-software
field: web-development
product: jekyll
tags: [jekyll-env, production-build, conditional-content, config-overrides]
level: practitioner
status: docs-checked
description: "Use JEKYLL_ENV and jekyll.environment to show content only in some builds, and layer config files per environment with --config."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/environments.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pass an environment to `build` or `serve` and test it in Liquid:

```liquid
{% if jekyll.environment == "production" %}
   {% include disqus.html %}
{% endif %}
```

The block only runs when you build with the matching value:

```sh
JEKYLL_ENV=production jekyll build
```

The default is `development`, so omitting `JEKYLL_ENV` means content inside `jekyll.environment == "development"` appears.

Values can be anything, not just `development` or `production`. Typical uses: hide Disqus comment forms or Google Analytics in development; show an "Edit me in GitHub" button in development but not production.

Setting the variable on the command line avoids editing config files when moving between environments.

To switch config settings by environment, list several files; later files override earlier ones:

```sh
jekyll build --config _config.yml,_config_development.yml
```

## Checked

2026-11-04. Confirmed against the Jekyll environments doc: `jekyll.environment` conditional, `JEKYLL_ENV=production jekyll build`, default `development`, arbitrary values, the Disqus, Google Analytics and edit-button examples, and layered `--config` files where later files win. Nothing removed.

Method: documentation only; no commands were run.
