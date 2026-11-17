---
id: computing-software.software-engineering.perl.common-traps-perltrap
name: common-traps-perltrap
category: computing-software
field: software-engineering
product: perl
tags: [perl, perltrap, common-mistakes, gotchas, context-mistakes, perl-pitfalls, common-traps-perltrap]
level: practitioner
status: docs-checked
description: "Recognise and avoid the usual Perl traps: ==/eq, list assignment, my in conditionals, map braces, sort, local, and awk/C/shell carry-overs."
sources: ["https://perldoc.perl.org/perltrap", "https://perldoc.perl.org/perlfaq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common traps (perltrap)

**Goal:** a checklist of mistakes seen constantly in reviews.

1. `==` on strings and `eq` on numbers: `"abc" == "def"` is true (both 0). Use `eq` for text.
2. `if ($x = 5)` assigns. Use `==`. (Perl warns only sometimes.)
3. `my $x = <$fh>` reads one line; `my ($x) = <$fh>;` reads all lines, keeps the first; `my @x = <$fh>` reads all.
5. `return` list vs scalar context; `return (1,2)[1]`; `return wantarray ? ... : ...`.
6. `my $x = $y if $cond;` undefined behaviour; declare first.
7. `foreach` loop variable aliasing modifies the array; `map { s/x/y/; $_ }` modifies the source.
8. `$h{$a, $b}` joins keys with `$;` (multi-dimensional emulation); use `$h{$a}{$b}` or `join`.
9. `split` with a string pattern is still a regex: `split '.', $s` splits on every char; `split '|'`.
10. `keys`/`each` order is random; `sort` is stringwise by default.
11. `@a = (1,2,3); $b = @a;` count vs `($b) = @a;` first element.
12. `if (@a == 0)`, not `if ($#a == 0)`; `$#a` is the last index.
13. `local` is not `my`; forgetting `local $_`/`$/` leaks to callers.
14. Unchecked `open`/`close`/`system`.
15. `chomp(my $line = <STDIN>)` warns on EOF if undef; use `// ''`.
17. Octal literals: `chmod 755` is decimal 755; write `0755`.
18. `print "yes" if $str == "abc"` numeric warning.
21. `&&` vs `and` precedence in assignment: `my $ok = $a and $b` assigns `$a` only.
24. `sort { $a <=> $b } @x` inside a package other than `main` is fine, but `my ($a, $b)` breaks it.
25. `-f $dir/$file` parses `$dir/$file` as division: write `-f "$dir/$file"`.

Source: perltrap lists differences from awk, C, shell and sed, and traps for newcomers.

## Self-check
- [ ] `perl -wle 'print "abc" == "xyz" ? "same" : "diff"'` prints `same` plus warnings: you know why.

## Checked
2026-11-02: confirmed against perltrap (it covers traps for newcomers from other languages), perlfunc (split, chomp, chmod/oct, wantarray, delete) and perlsyn/perldata (context, foreach aliasing, `$;`). Removed: items 4, 16, 19, 20, 22, 23, 26, 27 and the oct error claim.
Method: documentation only; no commands were run.
