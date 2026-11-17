---
id: computing-software.software-engineering.perl.regex-recursion-lexers
name: regex-recursion-lexers
category: computing-software
field: software-engineering
product: perl
tags: [perl, recursive-regex, pos-function, g-anchor, tokenizer, perlre, regex-recursion-lexers]
level: sme
status: docs-checked
description: "Match balanced constructs with (?R), (?1) and (?&name), and write tokenisers with //gc, pos() and G."
sources: ["https://perldoc.perl.org/perlre", "https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recursive patterns and \G lexers

**Goal:** the two advanced idioms: recursion and incremental lexing.

## Recursion
```perl
my $balanced = qr/ ( \( (?: [^()]++ | (?1) )* \) ) /x;     # (?1) recurses into group 1
"f(a(b)c)" =~ $balanced and print $1;                      # (a(b)c)

my $json_ish = qr/
  (?(DEFINE)
    (?<value>  \s* (?: (?&array) | (?&num) ) \s* )
    (?<array>  \[ (?: (?&value) (?: , (?&value) )* )? \] )
    (?<num>    -?\d+ )
  )
  \A (?&value) \z
/x;
```
`(?R)` (or `(?0)`) recurses to the beginning of the whole pattern; `(?PARNO)` recurses into a numbered capture group, with `(?-1)` and `(?+1)` relative; `(?&name)` recurses to a named group (the leftmost if names repeat; an undeclared name is an error; `(?P>name)` is an alias); `(?(DEFINE)...)` holds definitions whose yes-pattern is never directly executed. Captures set inside the recursion are not visible to the caller. Unlike PCRE and Python, Perl can backtrack into a recursed group. Possessive quantifiers and `(?>...)` stop backtracking, as in perlre's balanced-parens example.

## Tokeniser with \G and /gc
```perl
for ($input) {
    while (1) {
        if    (/\G\s+/gc)          { next }
        elsif (/\G(\d+)/gc)        { push @tok, [NUM => $1] }
        elsif (/\G([A-Za-z_]\w*)/gc) { push @tok, [ID  => $1] }
        elsif (/\G([-+*\/()])/gc)  { push @tok, [OP  => $1] }
        elsif (/\G\z/gc)           { last }
        else { die "bad input at " . pos() }
    }
}
```
With `/g` in scalar context each match continues from the previous one. A failed match normally resets the position to the start; `/c` avoids that, so the next alternative starts at the same place. `pos()` reads or sets the position and `\G` matches only at `pos()`. perlop calls `/\G.../gc` a useful idiom for lex-like scanners. perlre warns that `\G` used improperly can loop forever, especially in alternations.

## Failure modes
- Recursing deeply without consuming any input is a fatal error; a missing capture group for `(?PARNO)` is also fatal.
- Modifying the target string resets the search position.
- Modifiers such as `(?i)` are resolved at compile time and do not carry into a called subpattern.

## Self-check
- [ ] Every recursive call is preceded by consuming input, and the scanner has a final `\G\z` or error branch.

## Checked
2026-11-09. Read perlre's recursion section ((?PARNO), (?R), (?&NAME), DEFINE, possessive quantifiers, \G) and perlop's m//gc, /c and \G sections. Removed: the exact "Infinite recursion in regex" message, the HTML/XML/JSON parser advice and the perl -e self-check. The perlfunc pos entry was not read separately; pos behaviour is taken from perlop.
Method: documentation only; no commands were run.
