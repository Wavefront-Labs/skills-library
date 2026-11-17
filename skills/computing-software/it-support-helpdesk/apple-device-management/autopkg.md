---
id: computing-software.it-support-helpdesk.apple-device-management.autopkg
name: autopkg
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, app-automation, autopkg, recipes]
level: practitioner
status: docs-checked
description: "Build and run AutoPkg recipes and overrides to download, package and import Mac apps into Munki or other distribution systems, with trust checks."
sources:
  - "https://github.com/autopkg/autopkg/wiki"
  - "https://github.com/autopkg/autopkg/wiki/Overview-of-Using-AutoPkg"
  - "https://github.com/autopkg/autopkg/wiki/Preferences"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# autopkg

AutoPkg is a macOS automation framework: a recipe (plist or YAML) defines the steps to download software, extract it,
add site configuration and versioning, repackage it, and import it into a system such as Munki, Jamf Pro or FileWave.

## Workflow (Overview of Using AutoPkg)
1. Search for recipes: `autopkg search <term>`, autopkgweb.com, or GitHub search in the autopkg org.
2. Add recipe repos: `autopkg repo-add recipes` adds the core repo. Parent recipes may live in other repos; the error for
   a missing parent prints the `autopkg repo-add` command to fix it.
3. Create an override: `autopkg make-override FirefoxSignedPkg.pkg` writes a copy in `~/Library/AutoPkg/RecipeOverrides`
   (the default override directory; `--format yaml` or `RECIPE_OVERRIDE_FORMAT` gives YAML). Edit input variables in the
   override, for example the architecture to download. `-p` or `--pull` pulls missing parent repos and may need a GitHub
   token.
4. Run it: `autopkg run -v <override name>`; several recipes can follow one `run`, or use `--recipe-list FILE`.
   Overrides are searched before the recipe repos.
5. Maintain: after `autopkg repo-update`, a changed recipe no longer matches the trust information stored in the
   override and AutoPkg refuses to run it. Audit with `autopkg verify-trust-info -vv <override>` (the diff against what
   you last trusted), then record the new state with `autopkg update-trust-info <override>`.

## Trust
- Overrides store trust information on parent recipes and non-core processors (and, from AutoPkg 3.0.0, PkgCreator
  `scripts` files). Production recipes are expected to be overrides.
- Without trust info, runs only warn unless the `FAIL_RECIPES_WITHOUT_TRUST_INFO` preference is true.
- Preferences include `RECIPE_REPO_DIR` (default `~/Library/AutoPkg/RecipeRepos`) and `RECIPE_OVERRIDE_DIRS`.

## Practice
Keep overrides in version control, review `verify-trust-info` output before accepting changes, and read run output
regularly so a failed download or changed vendor URL is noticed quickly.

## Gotcha
Recipes run third-party processors, so trusting a changed parent recipe without reviewing the diff executes unreviewed
code.

## Checked

2026-11-09: confirmed on the AutoPkg wiki Home, Overview of Using AutoPkg, Preferences, Recipe Overrides and Getting
Started pages (read as raw markdown). Removed: JamfUploader and `.jamf` recipe claims, the Slack processor, launchd or CI
scheduling, the service account advice, cache-storage advice, and the Installomator and Munki wiki sources.

Method: documentation only; no commands were run.

## Verify
The run exits with the new package or import listed in its summary, and the item is present in the destination system.
