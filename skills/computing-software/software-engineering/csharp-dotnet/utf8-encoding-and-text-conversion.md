---
id: computing-software.software-engineering.csharp-dotnet.utf8-encoding-and-text-conversion
name: utf8-encoding-and-text-conversion
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-strings-text, utf8-encoding, encoding-getbytes, system-text-rune, bom, base64, invalid-utf8]
level: practitioner
status: docs-checked
description: "Handle UTF-8 in .NET: Encoding.UTF8 vs new UTF8Encoding, BOM, Span-based GetBytes/TryGetChars, invalid sequences, Rune and grapheme enumeration, Base64/hex helpers."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/base-types/character-encoding-introduction", "https://learn.microsoft.com/en-us/dotnet/api/system.text.unicode.utf8", "https://learn.microsoft.com/en-us/dotnet/api/system.text.rune"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UTF-8 encoding and text conversion

.NET strings are UTF-16; I/O boundaries are usually UTF-8.

## Convert
```csharp
byte[] bytes = Encoding.UTF8.GetBytes(text);
string s = Encoding.UTF8.GetString(bytes);
```
`System.Text.Unicode.Utf8` has span-based `FromUtf16` (UTF-16 chars to UTF-8 bytes) and `ToUtf16` (UTF-8 bytes to UTF-16 chars), each taking a destination span and reporting how many elements were read and written, and `IsValid(ReadOnlySpan<byte>)` to check that data is well-formed UTF-8.

## Characters vs code points vs graphemes
- A `char` is a UTF-16 code unit; a code point above U+FFFF is a surrogate pair (a high surrogate U+D800..U+DBFF followed by a low surrogate U+DC00..U+DFFF), so calling per-`char` methods such as `Char.ToUpperInvariant` on each `char` can split a pair.
- `System.Text.Rune` represents a Unicode scalar value (a code point that is not a surrogate); any `Rune` takes at most 2 `char` instances (`Rune.Utf16SequenceLength` gives the count). `text.EnumerateRunes()` iterates scalar values correctly.
- A user-perceived character (grapheme cluster) is a "text element" in .NET; use `StringInfo.GetTextElementEnumerator(text)` to enumerate them. A text element can be more than one scalar value.
- So `text.Length` (UTF-16 units), `EnumerateRunes().Count()` and the number of text elements can all differ for the same string.

## Checked
Date: 2026-11-09. Confirmed on the three cited Learn pages (character-encoding-introduction, Utf8 class, Rune): UTF-16 `char` and surrogate-pair ranges, `Rune` as scalar value with at most 2 `char`s, `EnumerateRunes`, `StringInfo` text elements, and the `Utf8.FromUtf16`, `ToUtf16`, `IsValid` members. Removed unconfirmed claims: BOM behaviour of `Encoding.UTF8`/`UTF8Encoding`, `File.WriteAllText` default, strict-decoding and `Decoder` advice, `OperationStatus` details, `Normalize`, Base64/hex helpers, `Encoding.Default` and code-page provider notes, `Substring` and `Utf8JsonReader` remarks, the verification test.
Method: documentation only; no commands were run.
