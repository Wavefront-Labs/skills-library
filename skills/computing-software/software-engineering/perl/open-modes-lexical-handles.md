---
id: computing-software.software-engineering.perl.open-modes-lexical-handles
name: open-modes-lexical-handles
category: computing-software
field: software-engineering
product: perl
tags: [perl, open, filehandle, three-arg-open, autodie, perlopentut, open-modes-lexical-handles, perl-file-io]
level: intro
status: docs-checked
description: "Open files with the three-argument form, lexical handles, encoding layers, error checks and close; use autodie."
sources: ["https://perldoc.perl.org/perlopentut", "https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlio"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# open modes, lexical filehandles and error checks

**Goal:** safe, readable file access.

```perl
open(my $in,  '<:encoding(UTF-8)', $path)  or die "Cannot read $path: $!";
open(my $out, '>:encoding(UTF-8)', $tmp)   or die "Cannot write $tmp: $!";
open(my $app, '>>', $log) or die ...;      # append
open(my $rw,  '+<', $path) or die ...;     # read/write without truncating
open(my $mem, '<', \$string);              # in-memory file
while (my $line = <$in>) { chomp $line; ... }
print {$out} "text\n";  printf $out "%d\n", $n;
close($out) or die "Close failed: $!";     # write errors (disk full) show up here
```

## autodie
```perl
use autodie;                     # open/close/unlink/etc. die on failure with a rich exception
eval { open(my $fh, '<', $f); 1 } or do { print "failed: $@" if $@->matches('open') };
```
`use autodie qw(:all)` also covers `system` and `exec`; `system` needs the optional IPC::System::Simple module.

## Rules
- Always the three-argument form; the two-argument form interprets leading/trailing characters in the name (`>`, `|`, spaces) and is a security risk.
- Bareword handles (`open(FH, ...)`) are global; use lexical `my $fh` which close automatically at scope end. From the 5.38 feature bundle (`use v5.38`) the `bareword_filehandles` feature is off, except for STDIN, STDOUT, STDERR, DATA, ARGV, ARGVOUT and `_`.
- `$!` holds the OS error only right after a failing call; copy it before running other code.
- Layers: `:raw` for binary, `:encoding(UTF-8)` for UTF-8 text. `binmode($fh, ':raw')` after open. On Windows text mode adds `:crlf` by default.
- Buffering: `$|=1` or `$fh->autoflush(1)` (before Perl 5.14, `use IO::Handle` first).

## Failure modes
- Forgetting to check `close` on write loses error information.

## Self-check
- [ ] `perl -e 'open(my $f,"<","/no/such") or print "err: $!"'` prints `err:` and the system error message.

## Checked
2026-11-03: confirmed against perlopentut and perlfunc (three-argument open, modes < > >> +<, in-memory files, encoding layers, close checks), autodie (lexical scope, matches, :all, system needing IPC::System::Simple), the feature documentation (bareword_filehandles exceptions) and perlport (:crlf text mode). Removed: the core-since-5.10.1 claim, strict-versus-lenient UTF-8 wording, the -e race bullet, rename pattern, user-input remark, exact errno message.
Method: documentation only; no commands were run.
