---
id: computing-software.web-development.jekyll.install-without-sudo
name: install-without-sudo
category: computing-software
field: web-development
product: jekyll
tags: [gem-home, user-gem-install, no-sudo, shared-hosting, bundle-path]
level: practitioner
status: docs-checked
description: "Run Jekyll as a non-superuser by pointing GEM_HOME at your home folder and updating PATH, which also fixes the not-allowed-to-install-to-system-RubyGems error."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On most Linux flavours, macOS and Bash on Ubuntu on Windows, you can run Jekyll without superuser rights and without installing gems system-wide. Add to the end of `.bashrc`:

```bash
# Ruby exports

export GEM_HOME=$HOME/gems
export PATH=$HOME/gems/bin:$PATH
```

This makes `gem` put gems in your home folder and places the local `jekyll` command ahead of system paths. It also helps on shared webhosting where accounts have limited privileges: add the exports before running `gem install jekyll bundler`.

Activate it by restarting Bash, logging out and in, or running `. .bashrc` in the current shell.

It solves this error from `jekyll new`:

```
Your user account is not allowed to install to the system RubyGems.
You can cancel this installation and run:

    bundle install --path vendor/bundle
```

Afterwards `jekyll new` should work for your account. The error text itself offers an alternative: install bundled gems into `./vendor/bundle/`.

## Checked

2026-11-04. Confirmed against the Jekyll Troubleshooting page, non-superuser section: .bashrc exports, shared hosting note, activation options and the jekyll new error text. Nothing removed.

Method: documentation only; no commands were run.
