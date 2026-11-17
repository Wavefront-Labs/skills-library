---
id: computing-software.software-engineering.perl.regex-named-captures
name: regex-named-captures
category: computing-software
field: software-engineering
product: perl
tags: [perl, named-captures, capture-groups, regex-captures, branch-reset, perlre, regex-named-captures]
level: practitioner
status: docs-checked
description: "Use (?<name>...) with %+ and %-, @- and @+ offsets, non-capturing groups, branch reset and K."
sources: ["https://perldoc.perl.org/perlre", "https://perldoc.perl.org/perlvar"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named captures and match arrays

**Goal:** readable captures that survive pattern edits.

```perl
if ($line =~ /^(?<ip>[\d.]+)\s+(?<method>[A-Z]+)\s+(?<path>\S+)/) {
    my %rec = %+;               # name => capture of the leftmost group of that name
    print "$+{ip} $+{method}\n";
}
my ($y,$m,$d) = $date =~ /^(\d{4})-(\d\d)-(\d\d)$/ or die;
(?:...)                 # non-capturing group: use for alternation without a capture
/(?|(\d+)-x|y-(\d+))/   # branch reset: both alternatives capture into $1
/foo\Kbar/              # \K keeps what precedes, so s/foo\Kbar/X/ turns foobar into fooX
```

## Match position arrays
- `$-[0]` and `$+[0]` are start and end offsets of the whole match; `$-[1]`, `$+[1]` of group 1.
- `$&`, `` $` `` and `$'` (match, prematch, postmatch) are safe to use from Perl 5.20, which enabled copy-on-write (perlvar); the `/p` flag and `${^MATCH}` remain available.
- `@{^CAPTURE}` (5.26+) lists all captures; `%-` holds arrays for repeated names.

## Rules and traps
- Capture group numbers count opening parentheses left to right; adding a group renumbers later ones. Named groups also get numbers.
- Quantified groups capture only the last repetition: `/(\w)+/` leaves the last char.
- Unmatched groups yield undef (perlvar: an optional group `(x)?` may be undef).
- `%+` is only valid in the scope of the last successful match.
- Duplicate names are allowed; `$+{name}` returns the leftmost defined.
- `/n` (5.22+) turns plain `(...)` into non-capturing so only named groups capture.

## Self-check
- [ ] `perl -e '"ab"=~/(?<x>a)(?<y>b)/; print "$+{x}$+{y} $-[2]"'` prints `ab 1`.

## Checked

2026-11-02. Confirmed in perlre and perlvar: `%+` leftmost defined group, `%-`, `@-`/`@+`, branch reset `(?|...)`, `\K`, `/p` with `${^MATCH}`; perl5200delta/perlvar: copy-on-write in 5.20 made `$&` safe; perl5260delta `@{^CAPTURE}`; perl5220delta `/n`. Removed: the unverified `defined $2` warning wording.

Method: documentation only; no commands were run.
