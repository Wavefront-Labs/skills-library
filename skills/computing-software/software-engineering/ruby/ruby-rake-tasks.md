---
id: computing-software.software-engineering.ruby.ruby-rake-tasks
name: ruby-rake-tasks
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, rake-tasks, build]
level: practitioner
status: docs-checked
description: "Write Rakefiles: task prerequisites, arguments, file and directory tasks, rules, namespaces, multitask and clean/clobber."
sources: ["https://raw.githubusercontent.com/ruby/rake/master/README.rdoc", "https://raw.githubusercontent.com/ruby/rake/master/doc/rakefile.rdoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rake tasks

A Rakefile is ordinary Ruby; anything legal in a Ruby script is allowed. Rake looks for `Rakefile` in the current directory, then parent directories, and runs all tasks from the directory containing it. Extra files named `*.rake` go in a `rakelib` directory next to the Rakefile (Rails also uses `lib/tasks`).

```ruby
require 'rake/clean'
CLEAN.include("tmp/*.o"); CLOBBER.include("dist")   # clean deletes CLEAN files; clobber also CLOBBER

desc "Run tests"                       # only described tasks appear in `rake -T`
task default: %w[test]

task :test do
  ruby "test/unittest.rb"
end

task :name, [:first_name, :last_name] => [:pre_name] do |t, args|   # args: open-struct like
  args.with_defaults(first_name: "John", last_name: "Dough")
  puts "#{args.first_name} #{args.last_name}"
end

file "prog" => ["a.o", "b.o"] do |t|   # file task; may be skipped if the file is up to date
  sh "cc -o #{t.name} #{t.prerequisites.join(' ')}"
end
directory "testdata/examples/doc"      # creates the directory chain on demand

multitask copy_files: %w[copy_src copy_doc copy_bin] do   # prerequisites run in parallel threads
  puts "All Copies Complete"
end

namespace "main" do
  task :build do; end
end
task build: %w[main:build]             # "main:build" addresses the task in a namespace
```
- A task may be defined more than once; each definition adds prerequisites and actions to the existing one.
- Arguments: `rake release[0.8.2]`, `rake name[john,doe]`; the name and arguments are one command-line argument, so quote it if it holds spaces: `rake "name[billy bob, smith]"` (quoting rules vary by shell). Extra arguments are ignored unless read via `args.extras`; `args.to_a` gives all in order.
- Rules synthesize tasks for missing files: `rule '.o' => ['.c'] do |t| sh "cc #{t.source} -c -o #{t.name}" end`. A rule with a regexp first argument needs parentheses. If a file exists with a task's name, Rake creates an implicit file task; `--rules` traces rule resolution.
- `import` loads a file after the main Rakefile but before targets run, so generated dependency files can be used in one run.
- Name resolution looks in the current namespace, then parents; a `^` prefix starts from the parent namespace and `rake:` refers to the top level. File and directory tasks are not scoped by namespaces.
- `FileList['*.rb']` behaves mostly like an array of strings.
- `rake -T` lists described tasks, `rake -P` prints tasks with prerequisites, `rake --help` lists all options. `Rake::Task[:name].clear` removes a task's prerequisites and actions (use with caution).

## Gotchas
- Use `do`/`end` for task and rule actions. With curly braces the block binds to the last method call (for example `object_files`) instead of `file`.
- With multitask, shared secondary prerequisites run once first, but user data shared between parallel prerequisites needs your own protection against races; Rake's own structures are thread-safe.
- The older `:needs` task-parameter format still works but is not recommended and may be dropped.
- A phony dependency for file tasks comes from `require 'rake/phony'`.

## Checked

Date: 2026-11-08. Read in full: the Rake README.rdoc and doc/rakefile.rdoc on GitHub. Removed: `rake -n` and `--trace`, `task.invoke`/`reenable` semantics, the unit-test and `:environment` advice, the `sh` multiple-arguments injection claim and its non-zero exit behavior, the zsh bracket quoting tip, and the ruby.github.io/rake source (not read).

Method: documentation only; no commands were run.
