---
id: computing-software.software-engineering.perl.perltidy-configuration
name: perltidy-configuration
category: computing-software
field: software-engineering
product: perl
tags: [perl, perltidy, perltidyrc, code-formatter, tidy-in-place, pbp-style, perltidy-configuration]
level: practitioner
status: draft
description: "Format Perl with perltidy: .perltidyrc options, in-place edits with backups, -pbp style and CI checks."
sources: ["https://metacpan.org/pod/Perl::Tidy", "https://perltidy.sourceforge.net/perltidy.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# perltidy configuration and editor integration

**Goal:** consistent formatting by tool, not by review comments.

```bash
cpanm Perl::Tidy
perltidy script.pl                       # writes script.pl.tdy
perltidy -b script.pl                    # in place, keeps script.pl.bak
perltidy -b -bext='/' script.pl          # in place, no backup file when the bext is "/" (use only under version control)
perltidy -st script.pl > out.pl          # to stdout
perltidy -pro=.perltidyrc lib/*.pm       # explicit profile
perltidy -pbp -nst file.pl               # Perl Best Practices style
perltidy -dpro                           # show the profile that would be used
cat file.pl | perltidy -se               # errors to stderr
```
`.perltidyrc` (current directory, then home; `PERLTIDY` environment variable overrides):
```
-l=100       # line length
-i=4         # indentation
-ci=4        # continuation indentation
-bar         # opening brace on same line
-nolq        # no outdent of long quotes
-ce          # cuddled else
-vt=2 -vtc=1 # vertical tightness
-nsfs        # no space for semicolon in for(;;)
-b -bext='/' # in place, no backup (editors/CI)
```

## Rules
- Pick one profile per repo, commit `.perltidyrc`, and pin the Perl::Tidy version in `cpanfile` (output changes between versions).
- CI check: run `perltidy` to a temp file and `diff`; fail on differences. A script such as `find lib t -name '*.p[lm]' -o -name '*.t' | xargs -n1 -I{} sh -c 'perltidy -st {} | diff -q - {}'` works.
- Use `#<<<` and `#>>>` comments to protect hand-formatted regions (format skipping is on by default in current versions; `-nfs` disables it).
- Editors: Vim `:%!perltidy`, Emacs cperl-mode + perltidy, VS Code Perl extensions with a formatter path; check each tool's documentation.
- Tidying the whole existing code base should be a separate commit so `git blame` can skip it (`.git-blame-ignore-revs`).

## Self-check
- [ ] Running perltidy twice yields no further changes (idempotent).
