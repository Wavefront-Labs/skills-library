---
id: computing-software.digital-forensics-incident-response.volatility.mapping-strings-to-processes-in-memory
name: mapping-strings-to-processes-in-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [strings-mapping, volatility3, windows-strings, memory-forensics, dfir]
level: practitioner
status: docs-checked
description: "Map strings found in a memory image back to owning processes with Volatility 3 windows.strings: producing offset files with Sysinternals strings and interpreting results."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.strings.html", "https://learn.microsoft.com/en-us/sysinternals/downloads/strings"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Mapping strings to processes in memory

Searching a memory image finds interesting strings (a C2 URL, a command line, a file name) but not who owned
them. Volatility 3's `windows.strings` reads the output of a `strings` command and indicates which
process(es) each string belongs to. Internally it builds a reverse mapping between virtual and physical
addresses, optionally limited to a list of PIDs, returning virtual offsets with strings and physical offsets.

## Step 1: extract strings with file offsets
Sysinternals Strings (`strings.exe`) scans a file for ASCII and Unicode strings (both by default, minimum
length 3). Relevant switches: `-o` prints the offset in the file at which a string was found, `-n` sets the
minimum length, `-a` is ASCII only, `-u` Unicode only.
```
strings -o -n 6 mem.raw > strings_all.txt
```
Check `vol windows.strings -h` for the exact input file option and the offset format your version expects
(the plugin reference does not list options).

Filter to the strings you care about before mapping to reduce noise and run time.

## Step 2: map
```bash
vol -f mem.raw windows.strings --help
```
Run the plugin with your strings file as its help text describes. The output associates each string with the
process(es) whose virtual address space maps that physical page.

## Interpreting
- A C2 URL mapped to an unexpected process is a lead; follow up with `windows.malware.malfind` or
  `windows.vadinfo` on that PID.
- Strings with no mapping sit in memory not mapped by any scanned process (for example freed pages or cache):
  residual, not necessarily active. Say so.

## Gotchas
- Very large strings files make the plugin slow; filter first.
- A string found by offset search that is not present when you dump the process region at the reported
  virtual address should not be reported.

## Verify
For each mapped string you report, dumping the process region at the given virtual address shows the same
string.

## Checked
2026-11-08. Read: windows.strings plugin reference page (purpose and generate_mapping) and the Sysinternals
Strings page (usage, switches, defaults). The GNU binutils strings page failed to load and was dropped as a
source. Removed unconfirmed claims: exact plugin option names (--strings-file, --pid), accepted offset line
formats, output format, pagefile layer advice, multiple-PID explanation and the GNU strings commands.
Method: documentation only; no commands were run.
