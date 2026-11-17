---
id: computing-software.software-engineering.perl.utf8-source-encoding-io
name: utf8-source-encoding-io
category: computing-software
field: software-engineering
product: perl
tags: [perl, use-utf8, encode-decode, open-pragma, perlunitut, encoding-layers, utf8-source-encoding-io, perl-unicode]
level: practitioner
status: docs-checked
description: "Handle UTF-8 correctly: use utf8 for source, decode input, encode output, set :std layers, and the -C switch."
sources: ["https://perldoc.perl.org/perlunitut", "https://perldoc.perl.org/perluniintro", "https://perldoc.perl.org/perlunifaq", "https://perldoc.perl.org/open", "https://perldoc.perl.org/perlrun", "https://perldoc.perl.org/Encode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Source encoding and Unicode I/O

**Goal:** characters inside, bytes at the edges.

```perl
use v5.36;
use utf8;                                       # the source file is UTF-8
use open qw(:std :encoding(UTF-8));             # STDIN/OUT/ERR and default layers for open
# or explicitly:
binmode(STDOUT, ':encoding(UTF-8)');
open(my $fh, '<:encoding(UTF-8)', $file) or die $!;
use Encode qw(decode encode);
my $text  = decode('UTF-8', $bytes, Encode::FB_CROAK);   # bytes -> characters
my $bytes = encode('UTF-8', $text);                       # characters -> bytes
```
```bash
perl -CSDA -e '...'      # -C flags: S=STDIN/STDOUT/STDERR, D=default open layers, A=@ARGV elements are utf8
export PERL_UNICODE=SDA  # same via environment
```

## Rules
- Three steps: decode on input, process as characters, encode on output. All communication outside the Perl process is bytes. If the input is binary and stays binary, do not decode it.
- "Wide character in print" is warned when you print a character above 255 to a handle with no encoding layer; Perl then outputs UTF-8 anyway. Always give the handle an explicit encoding layer, e.g. `binmode STDOUT, ":encoding(UTF-8)"`.
- `use utf8` only affects how the source is read (string literals, identifiers, delimiters); it does not change input or output.
- Use the strict name `UTF-8`, not `utf8`, for data exchange: `utf8` is Perl's liberal variant, and `decode_utf8`/`encode_utf8` are the `utf8` forms. Use `:encoding(UTF-8)` rather than `:utf8` when reading, because `:utf8` does not validate input and can cause security problems.
- Pass a CHECK argument such as `Encode::FB_CROAK`. Without it (`FB_DEFAULT`, 0) malformed data is replaced, on decode with U+FFFD.
- `length` and `substr` count characters on decoded text strings and bytes on encoded byte strings. Get a byte length after encoding.
- `use feature 'unicode_strings'` (enabled by `use v5.12` or later and by `-E`) makes the built-ins and regexes apply Unicode rules to characters 128 to 255 whether or not the string is internally UTF-8.
- You cannot tell a text string from a byte string by looking at the UTF8 flag; do not use `utf8::is_utf8` for that, and avoid `use bytes` and `use encoding`.
- `-C` with no value (or an empty `PERL_UNICODE`) equals `-CSDL`, which applies the layers only when the locale variables indicate UTF-8. `-C` and `PERL_UNICODE` do not validate input, and `-C0` or `PERL_UNICODE=0` disables them.
- `use open ':std', ...` changes the global standard handles, not just the lexical scope. Before Perl 5.34 `:std` applied only the first layer given.
- Undecoded bytes combined with text are silently treated as ISO-8859-1, which produces double encoding.

## Self-check
- [ ] `perl -CS -Mutf8 -e 'print length("é"), " é\n"'` prints `1 é`.

## Checked

Confirmed on the cited perldoc pages (perlunitut, perluniintro, perlunifaq, open, perlrun, Encode): decode/process/encode flow, wide character warning, use utf8 scope, :std behaviour and the 5.34 change, -C letters and PERL_UNICODE, FB_CROAK and FB_DEFAULT behaviour, UTF-8 vs utf8, unicode_strings, latin-1 upgrade. Removed (not in the pages): the JSON::PP utf8 note, filename and Windows handling, DBD driver flags, the `Encode::encode(locale_fs ...)` advice and the claim that Perl silently uses two bytes for an undecoded literal.

Method: docs-only read of cited pages, 2026-11-08
