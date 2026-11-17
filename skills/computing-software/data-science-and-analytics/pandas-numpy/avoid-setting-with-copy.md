---
id: computing-software.data-science-and-analytics.pandas-numpy.avoid-setting-with-copy
name: avoid-setting-with-copy
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [setting-with-copy, chained-assignment, copy-on-write]
level: practitioner
status: docs-checked
description: "Prevent silent write failures by assigning with one loc call, copying explicitly, and enabling Copy-on-Write behaviour where available."
sources:
  - https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SettingWithCopy and Copy-on-Write
Bad: `df[df.a > 1]["b"] = 0` is chained indexing; the assignment may land on a temporary.
Good: a single `df.loc[df.a > 1, "b"] = 0`; or take an explicit copy with `.copy()` and modify that.
## Gotchas
- The pandas indexing guide states that Copy-on-Write is the new default with pandas 3.0, which means chained indexing will never work: the parent frame is not updated.
- On earlier versions, check the release notes for the Copy-on-Write option before relying on either behaviour.
## Verify
- [ ] Re-read the parent frame and confirm the targeted rows changed.
## Checked
2026-11-02. Confirmed against the pandas user guide "Indexing and selecting data" (section "Why does assignment fail when using chained indexing?"): Copy-on-Write default in pandas 3.0 and chained indexing never working. Removed: the `pd.options.mode.copy_on_write` line and the SettingWithCopyWarning advice (the Copy-on-Write page could not be read, the indexing page does not state them).
Method: documentation only; no commands were run.
