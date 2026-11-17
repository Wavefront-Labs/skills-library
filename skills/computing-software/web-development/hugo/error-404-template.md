---
id: computing-software.web-development.hugo.error-404-template
name: error-404-template
category: computing-software
field: web-development
product: hugo
tags: [404-page, error-template, multilingual-404, hosting-redirect]
level: intro
status: docs-checked
description: "Create a 404 error page template in layouts, name it per language in multilingual projects, and know that the host decides how it is served."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/404.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a 404 template in the root of `layouts`:

```go-html-template
{{ define "main" }}
  <h1>404 Not Found</h1>
  <p>The page you requested cannot be found.</p>
  <p>
    <a href="{{ site.Home.RelPermalink }}">
      Return to the home page
    </a>
  </p>
{{ end }}
```

For multilingual projects add the language key to the file name:

```tree
layouts/
├── 404.de.html
├── 404.en.html
└── 404.fr.html
```

Your production server redirects the browser to the 404 page when a page is not found. Capabilities and configuration vary by host. GitHub Pages does this automatically and it is not configurable. The page links to host-specific instructions for Amazon CloudFront, Amazon S3, Apache, Azure Static Web Apps, Azure Storage, Caddy, Codeberg Pages, Cloudflare Pages, DigitalOcean App Platform, Firebase, GitLab Pages, NGINX and Netlify.

## Checked

2026-11-04: layouts/404.html example, per-language file names, host behaviour and host list confirmed against the Hugo docs Custom 404 page. Removed a cross-reference sentence about the development server that the page does not state.

Method: documentation only; no commands were run.
