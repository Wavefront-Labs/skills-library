---
id: computing-software.web-development.jekyll.default-configuration
name: default-configuration
category: computing-software
field: web-development
product: jekyll
tags: [default-config, config-defaults, directory-settings, kramdown-defaults, path-values]
level: practitioner
status: docs-checked
description: "Recall Jekyll's default configuration values (source, destination, exclude, markdown, port, permalink, liquid, kramdown) and how path settings resolve."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/default.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defaults apply unless overridden in the config file or on the command line.

Path rule: directory values such as `plugins_dir` are relative to the current working directory, not the site source. The `sass` key is the exception; its values are relative to the site source.

Key defaults from the page:

```yaml
source              : .
destination         : ./_site
collections_dir     : .
plugins_dir         : _plugins
layouts_dir         : _layouts
data_dir            : _data
includes_dir        : _includes
sass:
  sass_dir: _sass
collections:
  posts:
    output          : true
safe                : false
include             : [".htaccess"]
exclude             : ["Gemfile", "Gemfile.lock", "node_modules", "vendor/bundle/", "vendor/cache/", "vendor/gems/", "vendor/ruby/"]
keep_files          : [".git", ".svn"]
encoding            : "utf-8"
markdown_ext        : "markdown,mkdown,mkdn,mkd,md"
markdown            : kramdown
highlighter         : rouge
excerpt_separator   : "\n\n"
port                : 4000
host                : 127.0.0.1
baseurl             : ""
permalink           : date
paginate_path       : /page:num
future              : false
unpublished         : false
liquid:
  error_mode        : warn
  strict_filters    : false
  strict_variables  : false
kramdown:
  auto_ids          : true
  input             : GFM
  hard_wrap         : false
```

`plugins_dir` takes an array of strings and loads plugins in that order.

## Checked

2026-11-04. Compared every value in the YAML block, the path rule and the `sass` exception, and the `plugins_dir` comment with the Jekyll default configuration page. The block is a subset of the page's full list. Nothing removed.

Method: documentation only; no commands were run.
