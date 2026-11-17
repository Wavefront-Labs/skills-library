---
id: computing-software.systems-network-administration.bash.iconv-character-encoding
name: iconv-character-encoding
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, iconv, character-encoding, utf-8, latin1, windows-1252, utf-16, bom, file-encoding, uchardet, convmv, dos2unix, text-processing, sysadmin]
level: practitioner
status: gated
description: "Detect and convert text encodings on Linux: file -i and uchardet, iconv between UTF-8/Latin-1/CP1252/UTF-16, //TRANSLIT and -c, BOMs, CRLF, filename encodings with convmv, and verifying output."
sources:
  - https://man7.org/linux/man-pages/man1/iconv.1.html
  - https://man7.org/linux/man-pages/man1/file.1.html
  - https://www.gnu.org/software/libiconv/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iconv and character encodings

**Goal:** turn "Ã©" mojibake, `UnicodeDecodeError`s and Windows exports into clean UTF-8,
without silently losing characters.

## 1. Detect
```bash
file -i data.csv                    # text/plain; charset=iso-8859-1 (a guess)
uchardet data.csv                   # better heuristics (uchardet package); also: enca (neither was installed here (gated: unconfirmed, source is paywalled or blocked))
grep -axv '.*' data.csv | head      # in a UTF-8 locale: lines that are NOT valid UTF-8 (did not work with the MSYS grep 3.0 tested here (gated: unconfirmed, source is paywalled or blocked))
head -c 4 data.csv | xxd            # BOMs: ef bb bf = UTF-8, ff fe = UTF-16LE, fe ff = UTF-16BE
```
Detection is guessing; confirm by looking at known accented words in the output.
Western Windows exports are usually **CP1252** (a superset of Latin-1 with € and smart quotes) — prefer `-f CP1252` over `ISO-8859-1`.

## 2. Convert
```bash
iconv -f CP1252 -t UTF-8 in.csv > out.csv
iconv -f UTF-16LE -t UTF-8 export.txt > export.utf8.txt      # Excel "Unicode text"
iconv -f UTF-8 -t ASCII//TRANSLIT names.txt                  # transliteration is implementation/locale-dependent (GNU libiconv 1.17 tested: é → 'e, ß → ss)
iconv -c -f UTF-8 -t UTF-8 broken.txt > cleaned.txt          # drop invalid sequences (lossy — know what you drop)
iconv -l | grep -i 1252                                       # available names
```
iconv stops at the first invalid byte (libiconv 1.17 tested: `iconv: bad:1:3: cannot convert`, exit 1; glibc words it `illegal input sequence at position N` (gated: unconfirmed, source is paywalled or blocked))
— find it with `dd if=in bs=1 skip=N count=16 | xxd`. Never write output over the input file in the same pipeline (`> same-file` truncates first).
Batch: `for f in *.csv; do iconv -f CP1252 -t UTF-8 "$f" > "utf8/$f"; done`.

## 3. BOM and line endings
```bash
sed -i '1s/^\xEF\xBB\xBF//' file.csv        # strip UTF-8 BOM (breaks shebangs, some CSV parsers)
printf '\xEF\xBB\xBF' | cat - file.csv > excel.csv    # add one for Excel to open UTF-8 CSVs correctly
dos2unix file.txt                           # CRLF → LF (or sed -i 's/\r$//')
```

## 4. Filenames
Filenames are bytes; old archives/shares may use Latin-1 names that show as `?` in a UTF-8 terminal.
```bash
convmv -f iso-8859-1 -t utf-8 -r /srv/share            # dry run
convmv -f iso-8859-1 -t utf-8 -r --notest /srv/share   # do it
```
(convmv was not installed here (gated: unconfirmed, source is paywalled or blocked).) Mount options do the same for FAT/SMB: `iocharset=utf8` (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Double-encoded text ("Ã©" for "é") is UTF-8 that was decoded as Latin-1/CP1252 and re-encoded: reverse it with one `iconv -f UTF-8 -t CP1252` (tested: the bytes C3 83 C2 A9 become C3 A9, a correct UTF-8 é). Test on a sample first.
- `//TRANSLIT` results can depend on `LC_CTYPE` (glibc); with libiconv 1.17 the output was identical under `LC_ALL=C` and `en_US.UTF-8`.
- musl/BusyBox iconv supports fewer encodings than glibc (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `iconv -f UTF-8 -t UTF-8 out.csv > /dev/null` exits 0 (valid UTF-8); `file -i` reports utf-8.
- [ ] Row and byte counts make sense (`wc -l` equal before and after) and known accented values look correct.
