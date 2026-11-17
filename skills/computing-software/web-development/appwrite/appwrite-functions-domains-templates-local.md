---
id: computing-software.web-development.appwrite.appwrite-functions-domains-templates-local
name: appwrite-functions-domains-templates-local
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, functions, domains, templates, local-development, cli]
level: practitioner
status: docs-checked
description: "Expose functions on generated or custom domains, start from templates, and run them locally with appwrite run functions."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/domains/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/templates/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/develop-locally/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reach, start and iterate on functions.

Domains: each function gets a generated, region-specific domain ending `.appwrite.run`, shown under Functions > Domains; Appwrite generates TLS certificates for generated and custom domains. You can also add an `appwrite.network` edge domain, which routes to the nearest region. For a custom domain: Domains tab > Create domain > enter your domain > Next > copy the CNAME record to your domain registrar > Go to console. DNS records can take up to 48 hours to propagate; the domain is ready when VERIFICATION STATUS and CERTIFICATE STATUS are both green.

Templates: Console > your project > Functions > Templates lets you filter by search, use case or runtime; Create function opens a five-step wizard: Configuration, Variables, Connect (clone a new repository or connect an existing one), Repository, Branch. A pull request to the branch builds a deployment without activating it and gets a comment unless Silent mode is on.

Local development with the CLI: install Docker and keep it running, in a project with an `appwrite.config.json`, then run `appwrite run functions`. Flags from the docs: `--port` (defaults to 3000 or the closest available), `--function-id`, `--user-id <USER_ID>` (impersonates a user and sets the `x-appwrite-user-id` and `x-appwrite-user-jwt` headers if the user exists; the generated JWT lasts 1 hour), `--with-variables` (loads production environment variables; use only if your functions have no production secrets) and `--no-reload` (disable hot reload). Hot reload is on by default.

Gotcha: the domain is not usable until both statuses are green, which can take up to 48 hours after you add the CNAME.

The CLI prints `Visit http://localhost:3000/ to execute your function` when the runner starts.

Note: Docker replicates the production environment for local runs.


## Checked

2026-11-04. Confirmed against the Appwrite docs pages Domains, Templates and Develop locally: generated and edge domains, custom domain steps, the 48 hour propagation note and status colours, the templates wizard steps, the `appwrite run functions` requirements and each flag with its default, impersonation headers and JWT lifetime. Removed: the claim that dependency changes need a restart rather than hot reload, and the unverified "check DNS before assuming a certificate fault" advice.
Method: documentation only; no commands were run.
