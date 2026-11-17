---
id: computing-software.software-engineering.perl.os-differences-win32-portability
name: os-differences-win32-portability
category: computing-software
field: software-engineering
product: perl
tags: [perl, perlport, windows-perl, line-endings, platform-differences, os-differences-win32-portability, perl-portability]
level: practitioner
status: docs-checked
description: "Handle OS differences per perlport: $^O, newlines and binmode, file names, fork, alarm and list-form exec on Windows."
sources: ["https://perldoc.perl.org/perlport", "https://perldoc.perl.org/perlwin32", "https://perldoc.perl.org/perlfork"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing portable Perl and Windows specifics

**Goal:** one code base across Linux, macOS and Windows. Source: perlport.

```perl
if ($^O eq 'MSWin32') { ... }      # $^O values include darwin, MSWin32, cygwin (table in perlport)
use File::Spec::Functions qw(catfile updir);
my $file = catfile(updir(), 'temp', 'file.txt');   # builds paths with the right separator
binmode($fh);                      # no newline translation for binary data
use Config; $Config{osname};       # more detail than $^O, in %Config
```

## Differences to remember (perlport)
- `$^O` is set at build time to the OS name; it avoids loading `Config` just to read `$Config{osname}`. Use `%Config` for detail.
- Newlines: `\n` is the logical newline. In DOSish perls a file opened in text mode uses the `:crlf` layer, translating to and from `\015\012`. `binmode($filehandle)` keeps `\n` as `\012` and should always be used for binary data. Seeking and telling in text mode is limited: only seek to positions you got from `tell`, or use `binmode`. For network protocols use `use Socket qw(:DEFAULT :crlf);` rather than assuming `\n`.
- File names: some filesystems support neither hard nor symbolic links. NTFS is case-insensitive but case-preserving, so be careful with the case returned by `readdir` and used with `open`. For maximum portability do not have two files differing only in case and keep names to the 8.3 convention.
- Windows `alarm` is emulated with timers that are polled when Perl dispatches safe signals, so it cannot interrupt blocking system calls.
- Windows `fork` is emulated using multiple interpreters (see perlfork for its limits).
- The list form of `exec` and of piped `open` (`|-`, `-|`) is emulated on Win32 because `CreateProcess()` takes one command-line string, which may have security implications.
- Under Win32, `-l` returns true for both symlinks and directory junctions.
- Win32 module functions `Win32::GetOSVersion()`, `Win32::IsWinNT()` and `Win32::GetOSName()` identify the Windows version; `POSIX::uname()` is the very portable alternative.
- Windows glob quirks: `File::DosGlob` can override the internal `glob()` (perlwin32).
- CPAN Testers volunteers run uploaded modules on different platforms and report PASS, FAIL, NA or UNKNOWN; check the reports for portability.
- Build notes: perlwin32 covers building on Windows and mentions Cygwin as an alternative that gives a more Unix-compatible perl.

## Self-check
- [ ] Binary file handles use `binmode`; protocol code uses explicit CRLF constants.
- [ ] Tests ran on at least Linux and Windows.

## Checked
2026-11-09. Searched perlport, perlwin32 and perlfork for each claim; read the matching passages (newlines, file names, `$^O` table, per-function Win32 notes for alarm, fork, exec, open). Removed as not confirmed on these pages: Strawberry Perl contents and cpanm, ActiveState as recommendation, `File::Spec->tmpdir/devnull`, `File::HomeDir`, `$Config{path_sep}`/`ivsize`, flock and rename-open-file behaviour, `%ENV` case, `Win32::Unicode`, `Win32::LongPath`, `-CS`/`chcp`, `OS_UNSUPPORTED`, `Devel::AssertOS`, Path::Tiny, IPC::Run3.
Method: documentation only; no commands were run.
