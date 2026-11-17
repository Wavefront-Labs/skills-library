---
id: computing-software.web-development.jekyll.serve-command-options
name: serve-command-options
category: computing-software
field: web-development
product: jekyll
tags: [jekyll-serve, livereload, port-host, ssl-serve, detach, skip-initial-build]
level: practitioner
status: docs-checked
description: "Configure jekyll serve: port, host, livereload and its ignore/delay/port options, open-url, detach, skip initial build, directory listing and SSL key/cert."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/config_options/serve.yml
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`serve` accepts every `build` option; they apply to the build that runs just before serving.

- `-P, --port PORT` (`port`): default `4000`.
- `-H, --host HOSTNAME` (`host`): default `localhost`.
- `-l, --livereload` (`livereload`): reload the browser when content is edited.
- `--livereload-ignore GLOB1[,GLOB2]` (`livereload_ignore`): globs matched against each resource's `relative_path`. Quote them on the command line; if a quoted pattern still triggers reloads, list it in the config file.
- `--livereload-min-delay SECONDS` and `--livereload-max-delay SECONDS`: bounds on the reload delay (`livereload_min_delay`, `livereload_max_delay`).
- `--livereload-port PORT`: LiveReload port; overriding it in the config file (`livereload_port`) arrived in 4.4.0.
- `-o, --open-url` (`open_url`): open the site in a browser.
- `-B, --detach` (`detach`): detach from the terminal.
- `--skip-initial-build` (`skip_initial_build`): skip the build before the server starts.
- `--show-dir-listing` (`show_dir_listing`): show a directory listing instead of your index file.
- `--ssl-key` and `--ssl-cert`: private key and public certificate, stored or symlinked in the site source.

```sh
jekyll serve --livereload --livereload-ignore "GLOB1,GLOB2"
```

## Checked

2026-11-04. Confirmed against the Jekyll serve options data file and the configuration options page: every flag and config key listed, the `4000` and `localhost` defaults, the livereload ignore matching and quoting note, the 4.4.0 note on `livereload_port`, and that `serve` accepts the `build` options. Nothing removed.

Method: documentation only; no commands were run.
