---
id: computing-software.software-engineering.perl.printf-heredoc-formats
name: printf-heredoc-formats
category: computing-software
field: software-engineering
product: perl
tags: [perl, sprintf, printf, heredoc, here-document, perlform, printf-heredoc-formats]
level: practitioner
status: docs-checked
description: "Build text with sprintf/printf specifiers, indented heredocs (<<~), and know the legacy format/write feature."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlop", "https://perldoc.perl.org/perlform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sprintf, printf, here-documents and formats

**Goal:** formatted output without surprises.

```perl
printf "%-10s %5d %8.2f %s\n", $name, $count, $amount, $ok ? 'yes' : 'no';
my $s = sprintf('%05.1f|%+d|%x|%o|%b|%e', 3.14159, 42, 255, 8, 5, 1234.5);
my $t = sprintf('%2$s %1$s', 'world', 'hello');     # positional args
my $pct = sprintf('%.1f%%', 12.345);
sprintf('%s' x 3, @three);
sprintf('%*d', $width, $n);            # width from argument

print <<~EOT;                           # <<~ strips common leading indent (5.26+)
    Dear $name,
      indented line
    Total: @{[ sprintf '%.2f', $total ]}
    EOT
print <<'RAW';                          # single-quoted heredoc: no interpolation
$literal \n
RAW
```

## Rules
- `%s` is a string, `%d` a signed decimal integer, `%f` fixed-point, `%e` scientific, `%g` either, `%b` binary, `%x` hexadecimal, `%o` octal; Perl uses the C library only for floating-point conversions (perlfunc sprintf).
- Heredoc terminator must be alone on its line; with `<<~` it may be indented.
- Do not build SQL or shell commands with sprintf/heredocs from user data.
- `local $, = ","; local $\ = "\n";` change `print`'s separators.
- The older `format`/`write` report feature still exists (perlform).

## Self-check
- [ ] `perl -e 'printf("%05.1f|%-4s|\n", 3.14159, "ab")'` prints `003.1|ab  |`.

## Checked
2026-11-03: confirmed against perlfunc sprintf (conversions %s %d %u %o %x %e %f %g %b, flags, explicit index 2$, width from * argument, vector flag) and perlop (<<~ indented here-docs from Perl 5.26, quoted here-docs) and perlform. Removed: the %vd version-string example (the documented example is a different string), rounding claims, warning message names, East-Asian width modules, thousands-separator recipe and Number::Format.
Method: documentation only; no commands were run.
