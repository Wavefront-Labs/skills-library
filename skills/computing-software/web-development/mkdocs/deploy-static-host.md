---
id: computing-software.web-development.mkdocs.deploy-static-host
name: deploy-static-host
category: computing-software
field: web-development
product: mkdocs
tags: [static-hosting, scp, read-the-docs, deploy]
level: intro
status: docs-checked
description: "Host a MkDocs site on any static file server by copying the site directory (scp example), or via Read the Docs, which supports MkDocs out of the box."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/deploying-your-docs.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The output is static, so any provider that serves files works. Build, then copy the contents of `site_dir` (default `site`) to the server's root directory:

```sh
mkdocs build
scp -r ./site user@host:/path/to/server/root
```

Replace `user`, `host` and the path for your provider. Depending on the host you may use ftp, ssh or scp; search its docs for "ftp" or "uploading site".

If the host cannot map `X` to `X/index.html` (static S3 websites), set `use_directory_urls: false` (see `use-directory-urls`).

**Read the Docs** offers free hosting and supports MkDocs out of the box: arrange the repository per their instructions, create an account and point it at your publicly hosted repository; it updates on each push.

**GitHub Pages**: see `gh-deploy-project-pages`.

## Checked

2026-11-04. Confirmed against Deploying your docs (Other Providers, Read the Docs) and Getting Started (Deploying): `site_dir` default `site`, the scp example, ftp/ssh/scp, free Read the Docs hosting with out-of-the-box MkDocs support. Removed: a generic verify line.

Method: documentation only; no commands were run.
