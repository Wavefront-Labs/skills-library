---
id: computing-software.software-engineering.perl.file-tests-stat-dirs
name: file-tests-stat-dirs
category: computing-software
field: software-engineering
product: perl
tags: [perl, file-tests, stat, opendir, glob, readdir, file-find, file-tests-stat-dirs]
level: practitioner
status: docs-checked
description: "Test file attributes with -e -f -d -s -M, call stat, read directories with opendir, glob with bsd_glob, and walk trees with File::Find."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/File::Find", "https://perldoc.perl.org/File::Glob"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File tests, stat, directory reading and globbing

**Goal:** inspect the filesystem correctly.

```perl
if (-e $p && -f _ ) { ... }                 # `_` reuses the previous stat buffer
my @st = stat($p); my ($size, $mtime) = @st[7, 9];
my $mtime2 = (stat $p)[9];
opendir(my $dh, $dir) or die "$dir: $!";
my @files = grep { !/^\.\.?\z/ } readdir $dh;     # readdir includes . and ..
closedir $dh;
my @txt = glob("$dir/*.txt");                      # splits on whitespace
use File::Glob ':bsd_glob'; my @t = bsd_glob("$dir/my files/*.txt");   # safe with spaces
```

## File::Find
```perl
use File::Find;
find({ wanted => sub { return unless -f && /\.pm\z/; push @pm, $File::Find::name },
       no_chdir => 1 }, @dirs);
```
`$File::Find::name` is the full path; `$_` is the basename (and the cwd is the file's dir unless `no_chdir`). Use `finddepth` to process directories after their contents, `$File::Find::prune = 1` to skip a subtree.

## Rules
- `-M`/`-A`/`-C` are relative to `$^T` (script start), not now.
- `glob` splits its argument on whitespace; `bsd_glob` treats a space as part of a file name (File::Glob).

## Self-check
- [ ] `perl -e 'print -d "." ? "dir":"no"'` prints `dir`.

## Checked
2026-11-03: confirmed against perlfunc (file tests including the `_` handle, stat, opendir/readdir/closedir, glob), perlvar ($^T is the base for -M, -A, -C), File::Glob (bsd_glob and the :bsd_glob tag, space handling) and File::Find (find, finddepth, no_chdir, $File::Find::name, prune). Removed: the combined file-test comment line (rewritten below is not needed), Path::Tiny and File::Find::Rule, symlink and broken-link claim, readdir order claim, chmod octal remark, race remark and the return-count bullet.
Method: documentation only; no commands were run.
