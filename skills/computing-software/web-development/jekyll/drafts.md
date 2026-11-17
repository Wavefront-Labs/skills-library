---
id: computing-software.web-development.jekyll.drafts
name: drafts
category: computing-software
field: web-development
product: jekyll
tags: [drafts, drafts-flag, unpublished-posts, modification-time-date]
level: intro
status: docs-checked
description: "Keep unfinished Jekyll posts in _drafts without dates, preview them with --drafts, and know which date they take."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/posts.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/structure.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/front-matter.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/default.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Drafts are posts without a date in the filename: posts you are still writing and do not want to publish. Create a `_drafts` folder at the site root and add files named `title.MARKUP`:

```
.
├── _drafts
│   └── a-draft-post.md
```

Preview them by adding the `--drafts` switch to `jekyll serve` or `jekyll build` (config option `show_drafts`):

```sh
jekyll serve --drafts
```

Each draft is assigned the modification time of its file as its date, so the draft you are currently editing appears as the latest post.

Related: front matter `published: false` hides a single post, and `--unpublished` renders posts marked that way. Drafts is the folder-based approach; `published` is per-file.

## Checked

2026-11-04. Confirmed against the Jekyll posts doc (Drafts section), directory structure doc, front matter doc and default configuration page (`show_drafts`): date-less `title.MARKUP` drafts in `_drafts`, `--drafts` on `jekyll serve` and `jekyll build`, modification time used as the date, and `--unpublished`. Removed the sentence saying drafts are not rendered without the switch, which the page does not state.

Method: documentation only; no commands were run.
