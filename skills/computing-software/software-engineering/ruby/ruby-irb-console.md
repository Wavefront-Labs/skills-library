---
id: computing-software.software-engineering.ruby.ruby-irb-console
name: ruby-irb-console
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, irb-console, repl]
level: intro
status: docs-checked
description: "Use IRB: the irb executable, binding.irb breakpoints, debug gem integration, installing a newer IRB and where its docs live."
sources: ["https://github.com/ruby/irb"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IRB console workflow

IRB ("interactive Ruby") executes Ruby expressions read from standard input. Run `irb` from the shell to start a session; an input runs once it is syntactically complete (multi-line `class` definitions work, with `*` continuation prompts).

```ruby
# in your program (Ruby 2.5 or later): start a session in the surrounding context
def greet(word)
  binding.irb          # prompt shows local variables such as `word`; `exit` resumes the program
  puts "Hello #{word}"
end
```
- IRB is a default gem of Ruby, so no install is needed. To pin a specific version (Ruby 2.6 or later) add `gem 'irb'` to the Gemfile and run `bundle`, or run `gem install irb`.
- Debugging: inside `binding.irb`, the `debug` command starts an `irb:rdbg` session with access to all debug gem commands. Setting `RUBY_DEBUG_IRB_CONSOLE=1` makes the debug gem use IRB as its console.
- IRB v1.13.0 and later can be extended through official APIs (IRB Extension Guide).
- The README points to https://ruby.github.io/irb/ for the comprehensive guide and its Configuration page, and to a document comparing IRB with Pry; none of these pages was read for this check, so look up commands and `.irbrc` settings there.

## Gotchas
- Check the installed version first: features in the README depend on it (`binding.irb` needs Ruby 2.5 or later; extension APIs need IRB 1.13.0 or later).

## Checked

Date: 2026-11-08. Read in full: the IRB README on GitHub. Removed: all command lists (`ls`, `show_source`, `show_doc`, `edit`, `history`, `cd`), `.irbrc` settings, `_` and `__`, the `reload!` helper, the Rails console and production-data warnings, and the docs.ruby-lang.org IRB source (a stub), since the README does not state them.

Method: documentation only; no commands were run.
