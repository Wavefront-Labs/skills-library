---
id: computing-software.software-engineering.ruby.ruby-regexp-named-captures
name: ruby-regexp-named-captures
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, regexp-named-captures, regexp]
level: practitioner
status: docs-checked
description: "Use named captures, MatchData, string anchors and timeouts so Ruby regexes are readable and safe."
sources: ["https://docs.ruby-lang.org/en/master/Regexp.html", "https://docs.ruby-lang.org/en/master/MatchData.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regular expressions and named captures

```ruby
if (m = /(?<year>\d{4})-(?<mon>\d{2})/.match("on 2026-11-03"))
  m[:year]            # "2026"
  m.named_captures    # {"year"=>"2026", "mon"=>"11"}
end
# Literal on the left of =~ assigns local variables from names:
if /(?<user>\w+)@(?<host>[\w.]+)/ =~ "ann@example.org"
  puts user, host
end
```
Useful tools: `scan` (all matches), `gsub` with a hash or block, `String#match?` (no MatchData allocation, no `$~` side effects), `Regexp.union`, `Regexp.escape` for user text.

## Anchors
In Ruby `^` and `$` match at every line boundary. For validating a whole string use `\A` and `\z` (or `\Z` to tolerate a trailing newline). A pattern such as `/^\d+$/` accepts `"1\n<script>"`, a classic validation bypass.

## Catastrophic backtracking
For some patterns and inputs matching time grows polynomially or exponentially. Ruby applies a memoization optimization (added in 3.2) that makes matching linear when the pattern has no backreferences, no subexpression calls, no nested lookaround anchors or atomic groups, and no nested counted quantifiers; `Regexp.linear_time?(re)` tells you. The docs warn that input may still be unsafe, because memoization can use a lot of memory. When matching untrusted input set a timeout: `Regexp.timeout = 1.0` for the class default, or `Regexp.new(src, timeout: 1.0)` per regexp (an instance timeout overrides the class default; no timeout is set by default). A timed-out match raises `Regexp::TimeoutError`.

## Gotchas
- With named captures present, plain `( )` groups do not capture.
- Local-variable assignment from names happens only when the regexp literal is on the left of `=~`.
- `$~` and `$1` are thread-local and frame-local and the next match replaces them; copy values out immediately.
- `Regexp.new(user_input)` lets users supply their own pattern; escape with `Regexp.escape` unless that is intended.

Verify: `"1\nx".match?(/^\d+$/)` is true while `/\A\d+\z/` is false; `Regexp.linear_time?(/(a*)\1/)` is false.

## Checked
2026-11-03. Confirmed against ruby/ruby `doc/_regexp.rdoc` (anchors, named captures, timeout, optimization section), `re.c` rdoc (Regexp.new timeout, match? does not set matcher globals, MatchData#named_captures) and `doc/language/globals.md` (`$~` thread-local and frame-local). Fixed: the old text claimed `/(a+)+$/` is exponential and that the optimization makes "many patterns" linear; the docs give explicit criteria. Removed the timing exercise based on that pattern.
Method: documentation only; no commands were run.
