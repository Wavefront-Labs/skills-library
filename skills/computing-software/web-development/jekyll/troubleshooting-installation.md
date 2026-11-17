---
id: computing-software.web-development.jekyll.troubleshooting-installation
name: troubleshooting-installation
category: computing-software
field: web-development
product: jekyll
tags: [install-errors, ruby-dev-headers, xcode-command-line-tools, execjs-runtime, macos-sip, ffi-update]
level: practitioner
status: docs-checked
description: "Fix Jekyll install and run failures: Ruby dev headers per distro, Ubuntu Gemfile errors, macOS toolchain and SIP, ExecJS runtime errors, and old ffi on ARM64 Macs."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Gem compile errors usually need Ruby header files:

- Ubuntu/Debian: `sudo apt-get install ruby2.6-dev`
- Red Hat/CentOS/Fedora: `sudo yum install ruby-devel`
- Arch: `sudo pacman -S ruby-ffi`
- Gentoo (RubyGems): `sudo emerge -av dev-ruby/rubygems`
- Android with Termux: `apt update && apt install libffi-dev clang ruby-dev make`
- Windows: install the RubyInstaller DevKit.

On Ubuntu, "Could not locate Gemfile" or a `.bundle/` error after `bundle exec jekyll serve` means requirements are incomplete. Stock distributions need both packages: `sudo apt-get install ruby ruby-all-dev`.

macOS: run `gem update --system`; if that fails, `xcode-select --install`, then `gem install jekyll`. An out-of-date Xcode.app can interfere with the command line tools, so upgrade both. With System Integrity Protection (10.11+), either `gem install -n /usr/local/bin jekyll`, or install Ruby with Homebrew (`brew install ruby`), or use a version manager (RVM, rbenv, chruby). You may need `export PATH=/usr/local/bin:$PATH` (GUI apps: `launchctl setenv PATH "/usr/local/bin:$PATH"`). `/usr/local` is a "safe" location under SIP and avoids Apple's Ruby.

ARM64 macOS: `bundle exec jekyll serve` may fail with an old `ffi`; run `bundle update` or update `ffi` to at least `1.14.2`.

"Could not find a JavaScript runtime (ExecJS::RuntimeUnavailable)" from `jekyll-coffeescript`: install `nodejs` (or the `execjs` and `therubyracer` gems).

On Debian/Ubuntu you may need `/var/lib/gems/1.8/bin/` on your PATH for the `jekyll` executable.

## Checked

2026-11-04. Confirmed against the Jekyll Troubleshooting page: per-distro header packages, Ubuntu packages, macOS toolchain and SIP options, ffi 1.14.2, ExecJS runtime and the Debian/Ubuntu PATH note. Nothing removed.

Method: documentation only; no commands were run.
