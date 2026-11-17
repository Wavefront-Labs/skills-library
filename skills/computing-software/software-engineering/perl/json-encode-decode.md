---
id: computing-software.software-engineering.perl.json-encode-decode
name: json-encode-decode
category: computing-software
field: software-engineering
product: perl
tags: [perl, json, json-pp, canonical-json, json-encode-decode, perl-data-formats]
level: practitioner
status: docs-checked
description: "Encode and decode JSON with JSON::PP: UTF-8 handling, canonical output, booleans, number/string typing and bignum."
sources: ["https://perldoc.perl.org/JSON::PP"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON with JSON::PP

**Goal:** reliable JSON round-trips. JSON::PP is a pure-Perl, (almost) JSON::XS-compatible module and has been in the Perl core since 5.14.

```perl
use JSON::PP;
my $json = JSON::PP->new->utf8->canonical->pretty;
my $text = $json->encode({ name => 'x', list => [1, 2], ok => JSON::PP::true });
my $data = $json->decode($text);
my $data2 = decode_json($bytes);     # expects UTF-8 bytes; croaks on error
my $bytes = encode_json($data);      # same as JSON::PP->new->utf8->encode; returns UTF-8 bytes
```

## Rules (JSON::PP documentation)
- `->utf8` means encode produces, and decode expects, UTF-8 encoded bytes. With `->utf8(0)` encode returns a (non-encoded) Unicode string and decode expects one; any UTF-8/UTF-16 conversion is then done yourself, for example with `Encode`. `->ascii` escapes everything outside 0..127; `->latin1` escapes outside 0..255 and is mainly for binary data, a rare encoding for JSON.
- `->canonical` sorts object keys so the same data serialises identically; it adds comparatively high overhead. `->pretty` turns on indent, space_before and space_after. Without `canonical`/`sort_by`, key order is pseudo-random.
- Booleans: JSON true/false decode to `JSON::PP::true`/`false` (objects overloaded to act like 1 and 0); test with `JSON::PP::is_bool`, which on Perl 5.36+ also accepts Perl's core booleans. Encode as `JSON::PP::true`/`false`, or `\1` and `\0`. `core_bools` and `boolean_values` configure this.
- JSON null decodes to `undef`; `undef` encodes as null.
- Number versus string: a Perl scalar last used in a string context encodes as a JSON string, other defined scalars as numbers. Force a string with `"$x"`, force a number with `$x += 0`. JSON::PP 2.91_01 changed number detection; set `PERL_JSON_PP_USE_B` true to get the older behaviour.
- Infinity and NaN cannot be represented in JSON and passing them is an error. Validate data before encoding; JSON::PP trusts what you pass to `encode` but treats decoded text as tainted.
- Numbers: an integer that does not fit may be kept as a string (losing round-tripping); `->allow_bignum` converts big integers and any numeric values to `Math::BigInt`/`Math::BigFloat` objects.
- `->allow_nonref` is enabled by default since JSON::PP 4.0, so top-level scalars are allowed; all other flags default to disabled.
- Unblessed references other than `\0` and `\1` are errors; blessed objects need the object serialisation options.
- Incremental parsing: `->incr_parse` (works in void, scalar and list context).
- `JSON::PP` is the fallback when `JSON.pm` is used without `JSON::XS`; for speed, the page points to `Cpanel::JSON::XS` (a fork of JSON::XS) for JSON::PP-only flags.

## Checked
2026-11-09. Read JSON::PP sections: description, encode_json/decode_json, is_bool, utf8, ascii, latin1, canonical, allow_nonref, allow_bignum, incr_parse and the Perl to JSON and JSON to Perl mappings. Removed because the metacpan pages (JSON::MaybeXS, Cpanel::JSON::XS) are blocked and the claims are not on the JSON::PP page: JSON::MaybeXS backend selection and options, "maintained fork" statements, the builtin::true encoding claim, the 2**53 precision figure, error offset wording, "never eval JSON", and the command-line self-check.
Method: documentation only; no commands were run.
