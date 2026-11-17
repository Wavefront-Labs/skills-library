---
id: computing-software.software-engineering.rust.utf8-chars-graphemes-and-osstring
name: utf8-chars-graphemes-and-osstring
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-collections-strings, rust-utf8-text, utf8, unicode, graphemes, osstring]
level: practitioner
status: docs-checked
description: "Handle text correctly in Rust: byte vs char vs grapheme, safe slicing, from_utf8, unicode-segmentation, and OsString for non-UTF-8 platform strings."
sources:
  - https://doc.rust-lang.org/book/ch08-02-strings.html
  - https://docs.rs/unicode-segmentation/latest/unicode_segmentation/
  - https://doc.rust-lang.org/std/ffi/struct.OsString.html
  - https://doc.rust-lang.org/std/primitive.str.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# UTF-8, chars, graphemes and OsString

**Goal:** never slice in the middle of a character or assume a "character" is one `char`.

`String` is a wrapper around a vector of bytes and always valid UTF-8. A string can be viewed three ways: bytes, Unicode scalar values (what `char` is) and grapheme clusters (the closest thing to "letters"). The Book's Devanagari example `"नमस्ते"` is 18 bytes, six `char` values (the fourth and sixth are diacritics that mean nothing alone) and four grapheme clusters. Grapheme clusters are not in the standard library; use a crate such as `unicode-segmentation`.

```rust
let s = "नमस्ते";
s.len();                       // 18: bytes
s.chars().count();             // 6 scalar values
use unicode_segmentation::UnicodeSegmentation;
s.graphemes(true).count();     // 4 grapheme clusters (true = extended)
s.is_char_boundary(3);         // true if byte 3 starts a code point or is the end
s.get(0..3);                   // Option<&str>, None instead of a panic
String::from_utf8(bytes)?;     // Result<String, FromUtf8Error>
String::from_utf8_lossy(&bytes); // Cow<str>, invalid sequences replaced
s.char_indices();              // (byte offset, char) pairs
```

Indexing a string with a single number is rejected; a range slice like `&hello[0..1]` that cuts a character panics at runtime ("not a char boundary"). Be explicit: `chars()` for scalar values, `bytes()` for raw bytes.

Case: `str::to_lowercase` follows the Unicode standard (handles Greek sigma context) but not locale-specific casing such as Turkish and Azeri I. `eq_ignore_ascii_case` is an ASCII-only case-insensitive comparison without allocation.

## OsString
On Unix, OS strings are often arbitrary non-zero bytes (frequently UTF-8); on Windows, arbitrary non-zero 16-bit values (UTF-16 when valid). Rust strings are always valid UTF-8, so use `OsString` / `OsStr` for platform strings. `OsStr::to_str` returns `Option<&str>`; `to_string_lossy` returns a `Cow<str>` with invalid data replaced by the replacement character. The internal byte encoding is unspecified.

## Verify
Test with multi-byte and combining-mark strings; assert truncation never panics.

## Checked
2026-11-03. Confirmed against The Rust Book "Storing UTF-8 Encoded Text with Strings" (the 18/6/4 example, slicing panic, `chars`/`bytes`), the `str`/`String` pages (`is_char_boundary`, `get`, `char_indices`, `from_utf8`, `from_utf8_lossy`, `to_lowercase` locale note, `eq_ignore_ascii_case`), the unicode-segmentation crate page (`graphemes(true)`) and `OsString`/`OsStr` pages. Removed: `unicode-normalization`, `unicode-width`, `{:>5}` padding claim, WTF-8 and `CStr` claims, Windows path conversion remark.
Method: documentation only; no commands were run.
