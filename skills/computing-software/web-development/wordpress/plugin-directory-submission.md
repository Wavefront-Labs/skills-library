---
id: computing-software.web-development.wordpress.plugin-directory-submission
name: plugin-directory-submission
category: computing-software
field: web-development
product: wordpress
tags: [plugin-readme, wordpress-svn, plugin-directory, plugin-check, wordpress]
level: practitioner
status: docs-checked
description: "Publishing to the WordPress.org plugin directory: guidelines, Plugin Check, readme.txt rules, SVN trunk/tags/assets layout and releases."
sources:
  - https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/
  - https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/
  - https://developer.wordpress.org/plugins/wordpress-org/how-to-use-subversion/
  - https://wordpress.org/plugins/plugin-check/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin directory submission (SVN, readme.txt)

## 1. Before submitting
- Read the Detailed Plugin Guidelines. Guideline 17: a trademark or another project's name may not be the sole or initial term of a plugin slug without proof of ownership.
- Run the **Plugin Check** plugin and fix its findings before submitting.

## 2. readme.txt
```
=== Acme Notes ===
Contributors: acmeuser
Tags: notes, editorial, workflow
Requires at least: 6.5
Tested up to: 6.8
Requires PHP: 7.4
Stable tag: 1.2.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Short description, no more than 150 characters, no markup.

== Description ==
== Installation ==
== Frequently Asked Questions ==
== Screenshots ==
1. Caption for screenshot-1.png
== Changelog ==
= 1.2.0 =
* Added ...
== Upgrade Notice ==
```
- 1 to 5 tags (the guidelines count use of over 5 tags as spam); do not use competitors' plugin names as tags.
- `Stable tag` points to a folder in `/tags/`; once that tag exists, only its readme.txt is read, so changing trunk's readme.txt changes nothing on the plugin page.
- Since WordPress 5.8, `Requires at least` and `Requires PHP` are read from the main plugin file, not the readme.
- The version shown comes from the plugin's PHP header, not the tag folder name.

## 3. Submission and SVN
After approval you get an SVN repository:
```
/trunk      latest development code
/tags/1.2.0 immutable release copies
/assets     screenshots, header images and icons (not shipped to WordPress installs with the plugin)
```
```bash
svn co https://plugins.svn.wordpress.org/acme-notes
# copy files into trunk, then:
svn cp trunk tags/1.2.0
svn ci -m "Release 1.2.0" --username acmeuser
```
Update `Stable tag` and the plugin header `Version` together. SVN is a release channel, not a dev repo - commit releases, not every change.

Tag folder names should look like version numbers (2.0.1.3 is good, "Cool hotness tag" is bad).

## Checked
2026-10-31. Confirmed against the Detailed Plugin Guidelines (guideline 17 slug rule, over 5 tags is spam), How Your readme.txt Works (150-character short description, 1 to 5 tags, Requires headers read from the PHP file since 5.8, Stable Tag behaviour, version from the PHP header) and How to Use Subversion (trunk, tags, assets layout, `svn cp trunk tags/...`, version-like tag names). Removed: the "18 guidelines" count and bullet summary, `phpcs`, prefix length and bundled-library advice, asset file names, the readme validator, the 10up GitHub actions and the post-release paragraph.
Method: documentation only; no commands were run.

## Verify
- [ ] Plugin Check clean; Stable tag points to an existing tag; assets show on the plugin page.
