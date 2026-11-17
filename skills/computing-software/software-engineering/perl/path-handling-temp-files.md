---
id: computing-software.software-engineering.perl.path-handling-temp-files
name: path-handling-temp-files
category: computing-software
field: software-engineering
product: perl
tags: [perl, file-spec, file-temp, path-handling-temp-files]
level: practitioner
status: docs-checked
description: "Handle paths portably with File::Spec and create temp files and directories securely with File::Temp."
sources: ["https://perldoc.perl.org/File::Spec", "https://perldoc.perl.org/File::Temp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Portable paths and temp files

**Goal:** portable filesystem code with no hand-built slashes, and safe temporary files.

```perl
use File::Spec;
my $p   = File::Spec->catfile(@directories, $filename);   # also File::Spec::Functions' catfile
my $tmp = File::Spec->tmpdir();                            # system temp directory
my $nul = File::Spec->devnull();
my $abs = File::Spec->rel2abs($path);                      # relative to Cwd::cwd() unless $base given

use File::Temp qw(tempfile tempdir);
my $dir = tempdir(CLEANUP => 1);                           # removed at program exit
my ($fh, $filename) = tempfile(DIR => $dir, SUFFIX => '.dat', UNLINK => 1);
my $tmpf = File::Temp->new(SUFFIX => '.dat');              # object; file removed when it goes out of scope
my $tdir = File::Temp->newdir();                           # CLEANUP => 1 by default
```

## Rules (File::Temp)
- `tempfile` returns a filehandle and filename together; File::Temp says this prevents a race where another process creates the file between an existence check and the open. `tempfile` without a template places the file in `File::Spec->tmpdir`; `TMPDIR => 1` with a template does the same; `DIR` picks a directory.
- Prefer the filehandle: File::Temp advises not to look at or touch the filename at all, since checking it can only trigger more race conditions.
- `tempdir` does not remove the directory on exit unless you pass `CLEANUP => 1`; `File::Temp->newdir` cleans up when the object goes out of scope. A temp directory that is your current directory cannot be removed: `chdir` out first.
- The `File::Temp->new` object accepts `UNLINK` (default true), `DIR`, `EXLOCK`, `PERMS`, `SUFFIX` and `TEMPLATE`.
- `mktemp`-style functions that only return a name can suffer from race conditions; use the form that opens the file.
- The temp directory comes from `File::Spec->tmpdir`, which on some systems honours the `TMPDIR` environment variable; File::Temp notes this may not be secure and suggests `mkstemp` with an explicit template if that is a problem.
- Windows: if the `File::Spec::tmpdir` directory is not writable, File::Temp tries the user's local application data directory, or croaks.

## Self-check
- [ ] No code builds paths by concatenating `/` or `\`, and no code uses a predictable name in a shared temp directory.

## Checked
2026-11-09. Read File::Spec (catfile, devnull, tmpdir, rel2abs) and searched File::Temp for each option and security note above. Removed because their pages are not cited or readable: File::Basename, File::Copy, File::Path and Cwd specifics, all Path::Tiny usage (metacpan blocked), `File::Slurper`, the rename atomicity and `abs_path` symlink claims, and the shell self-check.
Method: documentation only; no commands were run.
