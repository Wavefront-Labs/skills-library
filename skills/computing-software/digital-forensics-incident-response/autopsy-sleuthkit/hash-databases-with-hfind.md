---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.hash-databases-with-hfind
name: hash-databases-with-hfind
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [hfind, hash-database, nsrl, sleuth-kit, known-files, dfir]
level: practitioner
status: docs-checked
description: "Index and query hash sets with The Sleuth Kit hfind (NSRL and md5sum formats), bulk lookups, and use the indexes with sorter to flag known-bad and skip known-good files."
sources: ["https://www.sleuthkit.org/sleuthkit/man/hfind.html", "https://www.sleuthkit.org/sleuthkit/man/sorter.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hash databases with hfind

`hfind` looks up hash values in a database using a binary search, so you can quickly tell whether a file is known. It works with the NIST National Software Reference Library (NSRL) and the output of `md5sum`.

## Index first
An index file must be created with `-i db_type` before a lookup works. `db_type` is `nsrl-md5` or `nsrl-sha1` for the NSRL (the difference is which hash the index is sorted by) or `md5sum` for home-made databases. The index is a sorted, fixed-length-entry file with two columns, hash and byte offset in the original file, and `hfind` seeks into the original database after a hit, so keep both files. The index is named from the database file plus hash type, for example `NSRLFile.txt-md5.idx` and `NSRLFile.txt-sha1.idx`.
```bash
hfind -i nsrl-md5 /usr/local/hash/nsrl/NSRLFile.txt
md5sum /bin/* /usr/bin/* > system.md5
hfind -i md5sum system.md5
```
`md5sum` databases can use either `MD5 (test.txt) = <hash>` or `<hash> test.txt` lines.

## Look up
```bash
hfind system.md5 76b1f4de1522c20b67acc132937cf82e      # hash on the command line
md5sum -q /bin/* | hfind system.md5                     # hashes on stdin
hfind -f bin.md5 system.md5                             # -f: file with one hash per line
hfind -q system.md5 <hash>                              # quick: 0 not found, 1 found; one hash at a time
```
`-e` prints extended information where the database type supports it. If both MD5 and SHA-1 indexes exist, both hash types can be supplied at run time.

## Using with sorter
`sorter` sorts files in an image into categories by type and can use hash databases, each of which must first be indexed for MD5 with `hfind`:
- `-a hash_alert`: known-bad database; matching files go into a special alert file.
- `-x hash_exclude`: known-good database; matching files are ignored.
- `-n nsrl_db`: the NSRL `NSRLFile.txt`; files found in it are ignored.
- `-d dir` writes results (required unless `-l` lists to stdout); `-i`, `-f` and `-o` give image type, file system type and sector offset.

## Gotchas
- Build an index per hash type you plan to use.
- Check line endings and hash formatting of homemade lists against the two accepted `md5sum` layouts before indexing.
- NIST changes the NSRL format over time; confirm the file you downloaded matches what `nsrl-md5` and `nsrl-sha1` expect.

## Verify
A known hash in the set returns a hit and one absent returns "Hash Not Found" before you rely on the index in casework.

## Checked
Checked 2026-11-09 against the hfind and sorter manual pages (synopsis, options, index naming, input types, examples). Removed: Hashkeeper, EnCase and TSK SQLite (.kdb) database claims and the `-n`/`-a` database creation commands, the Autopsy import statements, the specific RDSv3 statement, and the earlier `sorter -a -x ... -e` command (the manual defines `-a` as the alert database and `-e` as extension checking).
Method: documentation only; no commands were run.
