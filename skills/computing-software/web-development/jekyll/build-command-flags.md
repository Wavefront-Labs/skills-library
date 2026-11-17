---
id: computing-software.web-development.jekyll.build-command-flags
name: build-command-flags
category: computing-software
field: web-development
product: jekyll
tags: [build-flags, drafts-flag, future-flag, limit-posts, profile, strict-front-matter, trace]
level: practitioner
status: docs-checked
description: "Use jekyll build flags: --config, --drafts, --future, --unpublished, --limit_posts, --profile, --strict_front_matter, --baseurl, log level and quiet/verbose."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/config_options/build.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Build flags and their config-file options:

- `-w, --[no-]watch`: auto-regenerate on change.
- `--config FILE1[,FILE2]`: use these config files instead of `_config.yml`; later files override earlier.
- `-p, --plugins DIR1[,DIR2]` (`plugins_dir`) and `--layouts DIR` (`layouts_dir`): change those directories.
- `-D, --drafts` (`show_drafts`): render drafts.
- `--future` (`future`): publish future-dated posts or documents.
- `--unpublished` (`unpublished`): render unpublished posts.
- `--limit_posts NUM` (`limit_posts`): parse only that many posts.
- `--force_polling` (`force_polling`): force polling in watch.
- `-V, --verbose`, `-q, --quiet`: more or no output.
- `JEKYLL_LOG_LEVEL=info`: level among debug, info, warn, error.
- `JEKYLL_ENV=production`: select environment.
- `-I, --incremental` (`incremental`): experimental; rebuilds only changed files and may break generation in some cases.
- `--profile` (`profile`): Liquid rendering profile to find bottlenecks.
- `--strict_front_matter`: fail the build on a YAML syntax error in front matter.
- `--lsi`: related-posts index; needs the classifier-reborn plugin.
- `-b, --baseurl /PATH/TO/SITE` (`baseurl`): serve under a base path.
- `url: SCHEME://HOST[:PORT]`: canonical root URL with no trailing slash; combined with `baseurl` by `absolute_url`. Set to the localhost URL under `jekyll serve`.
- `-t, --trace`: full backtrace on error.
- `JEKYLL_NO_BUNDLER_REQUIRE=true`: skip requiring `:jekyll_plugins` gems.

## Checked

2026-11-04. Every flag, config key and environment variable compared with the Jekyll build options data file, including the config-file layering note, the incremental warning, the classifier-reborn requirement for `--lsi`, the `url` rules (no trailing slash, `absolute_url`, localhost under `jekyll serve`) and the log levels. Nothing removed.

Method: documentation only; no commands were run.
