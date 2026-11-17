---
id: computing-software.software-engineering.perl.perlcritic-policies
name: perlcritic-policies
category: computing-software
field: software-engineering
product: perl
tags: [perl, perlcritic, perlcriticrc, policy-severity, no-critic, static-analysis, perlcritic-policies]
level: practitioner
status: docs-checked
description: "Lint Perl with the perlcritic command: severity levels, themes, include/exclude, .perlcriticrc profiles, ## no critic annotations and output formats."
sources: ["https://metacpan.org/pod/perlcritic"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# perlcritic

**Goal:** run the Perl::Critic engine from the command line and tune which policies apply. Most policies come from Damian Conway's *Perl Best Practices*, but it is not limited to them.

```bash
perlcritic YourModule.pm                 # severity 5 only (the default)
perlcritic -4 lib/                       # severity >= 4; --stern is the same; directories are searched recursively
perlcritic -1 file.pm                    # everything; --brutal is the same
perlcritic --theme pbp file.pm
perlcritic --theme 'bugs && pbp' file.pm
perlcritic --top file.pm                 # top 20 violations by severity (implies severity 1)
perlcritic --include variables file.pm   # add policies matching /variables/imx
perlcritic --exclude strict file.pm      # exclude takes precedence over include
perlcritic --single-policy nowarnings file.pm   # just one policy, beats other selectors
perlcritic --profile project/perlcriticrc file.pm
perlcritic --list ; perlcritic --list-enabled ; perlcritic --list-themes
perlcritic --doc RequireBriefOpen        # perldoc of matching policies
perlcritic --statistics-only lib/ ; perlcritic -C lib/ ; perlcritic -l --single-policy X lib/
```
- Severity is 1 (least) to 5 (most severe); names gentle=5, stern=4, harsh=3, cruel=2, brutal=1. Setting `--theme` implicitly sets severity to 1 unless `--severity` is given. Number shortcuts: the most restrictive wins and an explicit `--severity` overrides them. Do not put a number shortcut directly after `--top`.
- `--verbose N|FORMAT` selects one of eleven formats (default 4, or 5 with multiple files); format 11 adds the policy and full diagnostic. Escapes include `%f %l %c %m %p %s %e %d %r`. Formats 1 to 3 suit editor integration.
- `--only` applies just the policies named in the profile; `--noprofile` ignores profiles; `--force` ignores `## no critic`; `--quiet` hides "source OK"; `--program-extensions .pl` treats files as programs. `--allow-unsafe` permits policies marked unsafe (all core ones are safe; third-party ones may execute code).

## Profile (.perlcriticrc)
Searched in the current directory, then the home directory; `PERLCRITIC` environment variable or `--profile` points elsewhere. INI syntax with `#` comments; settings before the first block are defaults for the options.
```ini
severity = 3
theme    = (pbp + security) * bugs
exclude  = Variables  Modules::RequirePackage

[TestingAndDebugging::RequireUseStrict]
severity = 5
[ControlStructures::ProhibitPostfixControls]
allow = if unless
severity = cruel
[Modules::RequireFilenameMatchesPackage]
add_themes = larry            # set_themes replaces a policy's themes
[-NamingConventions::Capitalization]   # leading '-' means never load it
```
`Perl::Critic::Policy::` may be omitted from names. Integer parameters accept underscores (`min_value = 1_000`). Policy parameters are documented per policy. The distribution includes `examples/perlcriticrc-conway`.

## Themes shipped
core, pbp, bugs, certrec, certrule, maintenance, cosmetic, complexity, security, tests. Combine with `&&` (and), `||` (or), `!` (not) and parentheses.

## Bending the rules
```perl
require 'Legacy.pl';  ## no critic            # on a code line: that line only
## no critic (EmptyQuotes, PostfixControls)   # until block end or "## use critic"
$foo = "";
## use critic
sub complicated_function {  ## no critic (ProhibitExcessComplexity)   # block policies: on the reporting line
```
- A bare `## no critic` disables all policies; always name policies. Arguments are bareword regexes in parentheses (no quotes), so a category like `NamingConventions` works. Annotations nest.
- Document-wide policies (for example `Documentation::RequirePodSections`) report at line 1, so the annotation cannot go there when a shebang is needed; disable them in the profile (affects all files).
- Use the smallest scope and try a compliant solution first.

## Self-check
- [ ] `perlcritic --list-enabled` shows the policies you expect and a deliberate violation is reported at the chosen severity.

## Checked
Method: 2026-11-08 read the full plain-text POD of the perlcritic command. The Perl::Critic page was not read, so its URL and the v1 claims about `equivalent_modules`, `RequireTidyCode`, Test::Perl::Critic, exit codes, add-on policy distributions and `cpanm` install were removed.
