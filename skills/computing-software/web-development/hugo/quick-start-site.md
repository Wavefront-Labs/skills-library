---
id: computing-software.web-development.hugo.quick-start-site
name: quick-start-site
category: computing-software
field: web-development
product: hugo
tags: [quick-start, new-project, theme-submodule, hugo-server, first-post]
level: intro
status: docs-checked
description: "Create a Hugo project with a theme, add a draft post, set baseURL and title in hugo.toml, preview with hugo server and publish to public."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/getting-started/quick-start.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Check the install with `hugo version`, then build a project with a theme as a Git submodule.

```sh
hugo new project quickstart
cd quickstart
git init
git submodule add https://github.com/gohugo-ananke/ananke themes/ananke
echo "theme = 'ananke'" >> hugo.toml
hugo server
```

Add content:

```sh
hugo new content content/posts/my-first-post.md
```

- The new file gets `title`, `date` and `draft = true` front matter. Hugo does not publish drafts by default.
- `hugo server --buildDrafts` (or `-D`) includes drafts in the preview. Set `draft = false` when the post is ready.
- Hugo follows the CommonMark specification for Markdown.

Configure `hugo.toml`, then restart the server:

```toml
baseURL = 'https://example.org/'
locale = 'en-us'
title = 'My New Hugo Project'
theme = 'ananke'
```

`baseURL` must begin with the protocol and end with a slash.

Publish with `hugo`. All output (HTML, images, CSS, JavaScript) goes to the `public` directory.

On Windows, run the commands from PowerShell or a POSIX shell (Bash in WSL or Git Bash), not Command Prompt or Windows PowerShell.

## Checked

2026-11-04: command sequence, draft behaviour and -D flag, CommonMark note, hugo.toml example, baseURL rule, publish to public and the Windows shell warning confirmed against the Hugo docs Quick start page. Nothing removed.

Method: documentation only; no commands were run.
