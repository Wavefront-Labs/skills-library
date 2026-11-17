---
id: computing-software.software-engineering.perl.regex-match-subst-operators
name: regex-match-subst-operators
category: computing-software
field: software-engineering
product: perl
tags: [perl, regex, match, substitution, perlre, perlop, regex-match-subst-operators, perl-regex-basics]
level: intro
status: docs-checked
description: "Use m//, s///, the g and c flags, list-context matching, /r and /e correctly, and the capture variables."
sources: ["https://perldoc.perl.org/perlre", "https://perldoc.perl.org/perlretut", "https://perldoc.perl.org/perlop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# m//, s/// and match variables

**Goal:** match, capture and substitute without the classic mistakes.

```perl
if ($s =~ /^(\w+)\s+(\d+)/) { my ($w, $n) = ($1, $2); }   # captures valid only after success
my ($w, $n) = $s =~ /^(\w+)\s+(\d+)/ or die "no match";     # list context returns captures
my @all  = $s =~ /\d+/g;                 # all matches (no groups)
my $cnt  = () = $s =~ /\d+/g;            # number of matches
while ($s =~ /(\w+)=(\w+)/g) { $h{$1} = $2 }    # iterate with pos()
(my $t = $s) =~ s/^\s+|\s+$//g;          # trim a copy
my $u = $s =~ s/foo/bar/gr;              # /r returns result, leaves $s (5.14+)
$s =~ s/(\d+)/$1 * 2/e;                  # /e evaluates the replacement as code
$s =~ s{/}{::}g;                         # alternative delimiters
my $n = ($s =~ s/x/y/g);                 # number of substitutions (or "" if none)
```

## Flags
`i` ignore case; `g` global; `m` ^/$ match at lines; `s` dot matches newline; `x` free-spacing; `e` evaluate; `r` return copy; `c` keep pos() after failed /g; `o` compile once (rarely needed).

## Gotchas
- `$1` etc. keep their value from the last **successful** match in the scope; a failed match does not reset them. Always test the match.
- Inside the replacement of `s///` use `$1`, not `\1` (perlop: `\1` is converted to `$1`).
- `$` matches before a trailing newline; use `\z` for the true end and `\A` for the start.
- `.` does not match "\n" without `/s`.
- Matching against `$_` is implicit: `/foo/` means `$_ =~ /foo/`.
- A pattern interpolating user input must be quoted: `/\Q$input\E/`.
- `split /,/` is not a match; `split` drops trailing empty fields unless limit is -1.
- Scalar `//g` in a loop on a changing string needs `pos($s) = 0` reset when you break out early.

## Self-check
- [ ] `perl -e '$_="a1b22"; @n=/\d+/g; print "@n"'` prints `1 22`.

## Checked

2026-11-02. Confirmed in perlop (m//, s///, flags c, g, e, r, o, `\1` converted to `$1`, pos reset on failed match, `/g` in scalar context) and perlre (`$` before trailing newline, `\A`/`\z`, `/s`); perl5140delta for `/r`; perlfunc for split dropping trailing empty fields. Reworded the `\1` deprecation claim.

Method: documentation only; no commands were run.
