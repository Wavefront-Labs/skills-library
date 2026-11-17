---
id: computing-software.web-development.jekyll.manual-deployment
name: manual-deployment
category: computing-software
field: web-development
product: jekyll
tags: [manual-deployment, rsync, s3-sync, ftp-upload, scp, rack-jekyll]
level: intro
status: docs-checked
description: "Deploy a built Jekyll _site by hand with rsync, aws s3 sync, FTP, scp or Rack-Jekyll, and where the output belongs on the host."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/deployment/manual.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Jekyll builds to `_site` by default. Transfer that directory's contents to almost any host.

- rsync: like scp but faster, since it only sends the changed parts of files.
- Amazon S3: use the AWS CLI to push the rendered directory to your bucket:

  ```sh
  aws s3 sync _site s3://<YOUR DOMAIN>.com --size-only --storage-class REDUCED_REDUNDANCY
  ```

- FTP: run `jekyll build`, then copy the contents of `_site` into the host's root folder, most likely `httpdocs` or `public_html`.
- scp (or direct filesystem access): same process; place the contents of `_site` in the web server's web root.
- Rack-Jekyll: deploys on any Rack server (Amazon EC2, Slicehost, Heroku and so on) and also runs under shotgun, rackup, mongrel, unicorn and others.

## Checked

2026-11-04. Confirmed against the Jekyll Manual Deployment page: rsync, S3 sync command, FTP, scp and Rack-Jekyll. Removed the closing sentence about the destination being cleaned on each build, which that page does not state.

Method: documentation only; no commands were run.
