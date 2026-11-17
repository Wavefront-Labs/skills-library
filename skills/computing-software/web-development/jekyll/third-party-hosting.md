---
id: computing-software.web-development.jekyll.third-party-hosting
name: third-party-hosting
category: computing-software
field: web-development
product: jekyll
tags: [hosting-options, netlify, gitlab-pages, aws-amplify, cloudcannon, deployhq, kickster]
level: intro
status: docs-checked
description: "Survey the hosting and deployment services the Jekyll docs list, with what each offers (CDN, continuous deployment, pipelines) and the Kickster option for GitHub Pages."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/deployment/third-party.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Services listed in the Jekyll docs:

- AWS Amplify: continuous deployment and hosting on every commit; CDN, custom domain with HTTPS, feature-branch deployments, redirects, password protection.
- CloudCannon: build, host and update Jekyll sites; global CDN, automated SSL, continuous deployment.
- DeployHQ: builds on its own infrastructure and transfers the rendered `_site/` over SSH, SFTP, FTP or to S3, Azure Blob or Rackspace. A typical pipeline runs `bundle install` then `bundle exec jekyll build`. Atomic releases, rollback, multiple environments per branch.
- GitHub Pages: free hosting powered by Jekyll.
- GitLab Pages: free hosting with custom domains and a customisable pipeline.
- KeyCDN: CDN with real-time image processing.
- Kickster: automated deploys to GitHub Pages when you use unsupported plugins; its Travis CI or Circle CI deployment scripts can be copied without the gem.
- Netlify: global CDN, continuous deployment, HTTPS, custom Jekyll plugins, free plan for open source.
- Render: zero-config continuous deployment for static sites.
- Vercel: zero-config continuous deployment, HTTPS custom domains, CDN.
- Hostman, 21YunBox, Layer0, Kinsta Application Hosting, Azion: hosting platforms with Jekyll guides.
- Supranode: customizable continuous deployment for static websites.
- Static Publisher: a server listening for webhook posts that publishes to S3 or a git repository.
- harvis: run `npx harvis` in `_site` after `jekyll build` to upload and get a URL.

Check each provider's own pricing and limits.

## Checked

2026-11-04. Confirmed against the Jekyll 3rd Party deployment page. Moved Supranode out of the list of providers with Jekyll guides, since the page gives it no Jekyll guide.

Method: documentation only; no commands were run.
