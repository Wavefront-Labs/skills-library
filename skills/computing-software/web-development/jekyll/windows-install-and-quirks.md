---
id: computing-software.web-development.jekyll.windows-install-and-quirks
name: windows-install-and-quirks
category: computing-software
field: web-development
product: jekyll
tags: [windows, rubyinstaller, devkit, tzinfo-data, wdm, utf8-bom, wsl]
level: practitioner
status: docs-checked
description: "Install Jekyll on Windows with RubyInstaller Ruby+Devkit or WSL, and handle encoding, time zone and auto-regeneration quirks with Gemfile entries."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/installation/windows.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Windows is not officially supported but works with tweaks.

RubyInstaller (2.4 and newer; older versions need the Devkit installed manually):

1. Install a Ruby+Devkit version, default options.
2. Run `ridk install` at the last stage of the wizard (needed for gems with native extensions); choose `MSYS2 and MINGW development toolchain`.
3. Open a new command prompt (so PATH changes apply) and run `gem install jekyll bundler`.
4. Check with `jekyll -v`; if it errors, reboot and run it again, and if it persists open a RubyInstaller issue.

Alternative: Windows Subsystem for Linux (Windows 10 version 1607 or later), then follow the Ubuntu installation procedure. The docs note that Bash on Ubuntu on Windows was still under development and may have issues.

Encoding: with UTF-8, Jekyll breaks if a file starts with a BOM; remove it. For `Liquid Exception: Incompatible character encoding` during site generation, run `chcp 65001` in the console.

Time zones: Windows has no native zoneinfo data, so Ruby does not understand IANA time zones. New sites from Jekyll 3.4 have the following in the `Gemfile` by default; existing sites must update their `Gemfile` and installed gems:

```ruby
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end
```

Auto-regeneration (`--watch`) uses the `listen` gem, which may need an extra gem on Windows. If you have issues with it, add to the `Gemfile`:

```ruby
gem "wdm", "~> 0.2.0", :install_if => Gem.win_platform?
```

Installing `wdm` needs the Ruby+Devkit version of RubyInstaller and the MSYS2 build tools.

## Checked
2026-11-09. Read the cited Jekyll "Jekyll on Windows" documentation page in full and compared each step, code block and caveat; the earlier draft matched it, so only wording was tightened and the omitted caveats (older RubyInstaller, WSL status, non-superuser pointer) were added or noted.
Method: documentation only; no commands were run.
