---
id: computing-software.software-engineering.ruby.ruby-optionparser-cli
name: ruby-optionparser-cli
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, optionparser-cli, cli]
level: practitioner
status: docs-checked
description: "Build a Ruby command-line tool with OptionParser: typed options, help text, required args and error handling."
sources: ["https://docs.ruby-lang.org/en/master/OptionParser.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command-line tools with OptionParser

```ruby
#!/usr/bin/env ruby
require "optparse"
opts = { verbose: false, count: 1 }
parser = OptionParser.new do |o|
  o.banner = "Usage: tool [options] FILE..."
  o.version = "1.0.0"
  o.on("-c", "--count N", Integer, "Repeat N times") { |v| opts[:count] = v }
  o.on("-f", "--format FMT", %w[json csv], "Output format") { |v| opts[:format] = v }
  o.on("-v", "--[no-]verbose", "Chatty output") { |v| opts[:verbose] = v }
  o.on("-h", "--help") { puts o; exit }
end
begin
  files = parser.parse!(ARGV)         # returns remaining positional args
  abort(parser.to_s) if files.empty?
rescue OptionParser::ParseError => e
  warn e.message; warn parser; exit 2
end
```
Built-in coercions include Integer (octal accepted), DecimalInteger, Float, Numeric, String, TrueClass/FalseClass, Array (comma-separated) and Regexp; Date, DateTime, Time, URI and Shellwords need `require "optparse/date"` (and `optparse/time`, `optparse/uri`, `optparse/shellwords`). Passing an Array (or an Array plus a Hash of aliases) as the type gives keyword completion: the user may type the shortest unambiguous text. Add your own conversion with `accept`.

## Gotchas
- `parse!` removes switches from the array it is given (ARGV by default) and leaves non-option arguments in it; `parse` works on a copy of an array argument.
- Without `POSIXLY_CORRECT` in the environment, options are parsed in permutation mode (options may follow positional arguments); with it set, parsing stops at the first non-option.
- `"-c", "--count N"` declares a required argument; a missing one raises `OptionParser::MissingArgument` and a bad value raises `OptionParser::InvalidArgument` (message `invalid argument: -t nonsense`), both `ParseError`s.
- Required options are not a built-in switch: check for them after parsing.
- Print error and usage text to stderr and choose your own non-zero exit status for usage errors.

Verify: run `tool --count x` and expect `invalid argument: --count x` followed by usage and exit status 2 (`echo $?`).

## Checked
2026-11-03. Confirmed against ruby/ruby `lib/optparse.rb` rdoc and source (banner, version, type coercion list and `optparse/*` requires, keyword completion with Array and Hash, `--[no-]` switches, `parse`/`parse!` and POSIXLY_CORRECT, MissingArgument and InvalidArgument messages). Removed: Symbol coercion, `required_arguments`, the 0/1/2 exit-code convention, and the abbreviation and `--` claims (not read in the docs).
Method: documentation only; no commands were run.
