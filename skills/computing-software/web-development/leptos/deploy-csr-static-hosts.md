---
id: computing-software.web-development.leptos.deploy-csr-static-hosts
name: deploy-csr-static-hosts
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, deployment, csr, trunk, github-pages, vercel, netlify]
level: practitioner
status: docs-checked
description: "Build a Leptos CSR app with trunk build --release and publish dist to GitHub Pages, Vercel, Netlify or Spin, including public-url and SPA redirect settings."
sources: [https://book.leptos.dev/deployment/csr.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy a client-side-rendered Leptos app

Goal: publish a Trunk-built CSR app as static files.

```bash
trunk build --release
```

This writes artifacts to `dist/`; publishing `dist` is all that is needed, like any JavaScript app.

## GitHub Pages

In repo settings, Pages, set source to "Github Actions". Add a workflow (for example `.github/workflows/gh-pages-deploy.yml`) triggered on push to main with `permissions` contents write, pages write, id-token write. Steps: checkout, install nightly Rust, `rustup target add wasm32-unknown-unknown`, download the Trunk release binary, then:

```
./trunk build --release --public-url "${GITHUB_REPOSITORY#*/}"
```

`--public-url` is needed because the site lives at username.github.io/repo_name; otherwise asset paths 404. Then `actions/configure-pages`, `actions/upload-pages-artifact` with path `./dist`, and `actions/deploy-pages`. The page suggests optionally copying `dist/index.html` to `404.html` so routing works when entering from any route.

## Netlify

Add `netlify.toml`:

```toml
[build]
command = "rustup target add wasm32-unknown-unknown && cargo install trunk --locked && trunk build --release"
publish = "dist"

[build.environment]
RUST_VERSION = "stable"

[[redirects]]
from = "/*"
to = "/index.html"
status = 200
```

and `rust-toolchain.toml` with `channel = "stable"` and `targets = ["wasm32-unknown-unknown"]`. Connect the Git repo in Netlify; the redirect makes SPA routes serve `index.html`.

## Vercel

In the Vercel UI create a project, leave Build Command empty (override on) and set Output Directory to `dist` (override on). For GitHub Actions deploys: create a Vercel access token (`VERCEL_TOKEN`), run `vercel login` and `vercel link`, read `projectId` and `orgId` from `.vercel/project.json` and store as `VERCEL_PROJECT_ID` and `VERCEL_ORG_ID` repo secrets. Production workflow builds with Trunk, then in `dist` runs `vercel deploy --prod --token=...`; a PR preview workflow uses `amondnet/vercel-action`.

## Spin (Fermyon Cloud)

Create a Fermyon Cloud personal access token, save it as the repo secret `FERMYON_CLOUD_TOKEN`, and use the `fermyon/actions/spin/setup`, `deploy` and `preview` actions (adds the `wasm32-wasi` target too).

Serving at a sub-path: computing-software.web-development.leptos.deploy-non-root-path.

Full workflow files are in the page; only the key steps are summarized here.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/deployment/csr.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
