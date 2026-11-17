---
id: computing-software.web-development.jekyll.command-plugins
name: command-plugins
category: computing-software
field: web-development
product: jekyll
tags: [command-plugins, jekyll-command, init-with-program, mercenary, jekyll-plugins-group]
level: sme
status: docs-checked
description: "Extend the jekyll executable with subcommands: subclass Jekyll::Command, implement init_with_program, and load the gem from the :jekyll_plugins Gemfile group."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/commands.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since 2.5.0, plugins can add subcommands to the `jekyll` executable. Include them in the `:jekyll_plugins` Gemfile group:

```ruby
group :jekyll_plugins do
  gem "my_fancy_jekyll_plugin"
end
```

Each command subclasses `Jekyll::Command` and has one class method, `init_with_program`, which receives the `Mercenary::Program` instance (the Jekyll program itself). Define commands on it:

```ruby
class MyNewCommand < Jekyll::Command
  class << self
    def init_with_program(prog)
      prog.command(:new) do |c|
        c.syntax "new [options]"
        c.description 'Create a new Jekyll site.'

        c.option 'dest', '-d DEST', 'Where the site should go.'

        c.action do |args, options|
          Jekyll::Site.new_site_at(options['dest'])
        end
      end
    end
  end
end
```

See the Mercenary repository on GitHub for the full command-definition API.

## Checked

2026-11-04. Confirmed against the Jekyll plugins Commands page: 2.5.0 gate, :jekyll_plugins group, Jekyll::Command subclass, init_with_program and the example. Removed the closing sentence about when plugin gems load, which the page does not state.

Method: documentation only; no commands were run.
