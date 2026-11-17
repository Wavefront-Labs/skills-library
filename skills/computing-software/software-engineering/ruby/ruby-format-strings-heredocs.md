---
id: computing-software.software-engineering.ruby.ruby-format-strings-heredocs
name: ruby-format-strings-heredocs
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, format-strings-heredocs, formatting]
level: intro
status: docs-checked
description: "Write Ruby heredocs (plain, dash, squiggly, quoted), escape sequences and percent literals, and avoid interpolation surprises."
sources: ["https://docs.ruby-lang.org/en/master/syntax/literals_rdoc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heredocs, string literals and percent literals

## Heredocs
```ruby
a = <<HEREDOC        # body starts on the next line, ends at a line starting with HEREDOC
text
HEREDOC
b = <<-EOS           # "-": the closing identifier may be indented; body indentation is kept
    body
    EOS
c = <<~SQL           # "~" squiggly: strips the indentation of the least-indented line
  SELECT *
    FROM users
SQL
d = <<-'RAW'         # single-quoted identifier: no interpolation and no escapes
  #{1 + 1}
RAW
e = <<-EOS.chomp     # call a method right after the opening identifier
  text
EOS
```
- The result includes the ending newline.
- A heredoc allows interpolation and the escape sequences; quote the opening identifier with single quotes to disable both. Double quotes mean the same as no quotes. Backticks make it behave like Kernel#`.
- With `<<-`, the content is treated as flush left: if you indent the content, those spaces appear in the output.
- For `<<~`, empty lines and lines of only literal tabs and spaces are ignored when working out the indentation, while escaped tabs and spaces count as non-indentation characters. A tab counts as one to eight spaces up to the next multiple of eight, and a tab cut by the removal boundary is not removed.
- Several heredocs can open on one line, `puts(<<-ONE, <<-TWO)`, but this is hard to read.

## Strings
- Double-quoted strings allow escape sequences and `#{...}` interpolation; `#@foo`, `#@@foo` and `#$foo` are shorthand for interpolating those variables.
- Single-quoted strings disable interpolation and every escape except `\'` and `\\`. Escaping the `#` also disables interpolation.
- Adjacent literals are concatenated: `"con" "cat"`, and a trailing backslash folds a line (`"a "\` newline `"b"`). A percent string may not come last: `"a" 'b' %q{c}` raises NoMethodError.
- Character literal: `?a` is `"a"`; `?abc` is a SyntaxError.
- Escapes include `\n \t \s \e \\`, `\nnn` (octal), `\xnn`, `\unnnn` and `\u{nnnn ...}`; `\<newline>` is an empty string (line fold).

## Percent literals
- `%q(...)` is non-interpolating like single quotes; `%Q(...)` or `%(...)` interpolates like double quotes. Brackets, parentheses, braces and angle brackets may nest if paired; other non-alphanumeric ASCII characters work as both delimiters.
- `%w[a b]` and `%i[a b]` build string and symbol arrays (no interpolation); `%W` and `%I` interpolate, and an interpolated value stays one word even with spaces. A backslash embeds a space in a word.
- `%s[foo]` is a symbol, `%r{...}` a regexp, `%x(cmd)` runs a shell command and interpolates.

## Gotchas
- Interpolating untrusted input into a `%x` shell string or a backtick heredoc is injection; the same applies to SQL text.
- `%w(#{1 + 1})` gives `["\#{1", "+", "1}"]`; use `%W` to interpolate.

## Checked

Date: 2026-11-08. Read in full: the Ruby syntax documentation for literals (the raw rdoc source of the page on GitHub). Removed: all `format`, `sprintf` and `String#%` directive claims (the Format Specifications page could not be fetched; the page is a stub at docs.ruby-lang.org), the `ArgumentError` and `$DEBUG` argument-count claims, the `%d` Float and String claims, and the claim about interpolated multi-line values inside squiggly heredocs, none of which were confirmed by a page I read.

Method: documentation only; no commands were run.
