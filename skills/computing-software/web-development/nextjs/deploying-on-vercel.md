---
id: computing-software.web-development.nextjs.deploying-on-vercel
name: deploying-on-vercel
category: computing-software
field: web-development
product: nextjs
tags: [vercel-deployment, preview-deployments, environment-variables, serverless-functions, nextjs]
level: practitioner
status: docs-checked
description: "Deploying Next.js on Vercel: Git and CLI deployments, environment variables per environment, function limits and regions, and deployment protection."
sources:
  - https://vercel.com/docs/deployments
  - https://vercel.com/docs/environment-variables
  - https://vercel.com/docs/functions/limitations
  - https://vercel.com/docs/deployment-protection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying on Vercel

Limits and plan details below are as the docs stated them when read; they change, so recheck the pages.

## 1. Deployment methods
- Git: importing a repository means each commit or pull request (on supported providers: GitHub, GitLab, Bitbucket, Azure DevOps) triggers a deployment, each with a unique URL. You can also deploy a specific Git reference from the dashboard.
- Vercel CLI: `vercel deploy` creates a preview deployment, `vercel deploy --prod` (or `vercel --prod`) a production one; it works with or without Git, and in CI. A `.vercel` directory stores project and organisation IDs. `vercel curl` and `vercel logs --deployment ...` help verify a deployment.
- Deploy Hooks (need a connected Git repository): an HTTP GET or POST to a unique URL triggers a deployment without a new commit.
- Vercel Drop and the REST API are also supported. On Pro and Enterprise teams a deployment policy can restrict which Git sources and mechanisms may deploy to each environment.
- Default environments: Local, Preview and Production. From the dashboard you can redeploy, inspect, assign a custom domain and promote a preview to production; Vercel documents a separate guide for rolling back a production deployment.

## 2. Environment variables
- Declared at team level (all projects) or project level. Each variable applies to one or more of Production, Preview, custom environments and Development. Values are encrypted at rest; Config values stay readable to members, Secret values are write-only after saving.
- Changes do not apply to previous deployments, only to new ones.
- Preview variables apply to any non-production branch; you can scope one to a specific branch, and branch-specific values override other preview values of the same name.
- Local development: `vercel env pull` writes the Development variables to a `.env` file; `vercel dev` loads them into memory.
- Size: 64 KB total per deployment on the Node.js, Python, Ruby and Go runtimes; edge runtime functions and Middleware are limited to 5 KB per variable.

## 3. Functions (with Fluid compute)
- Maximum duration: Hobby 300 s (default and maximum); Pro and Enterprise 300 s default, 800 s maximum, with a beta 1800 s extended maximum. Set with the `maxDuration` config; a timeout returns 504 `FUNCTION_INVOCATION_TIMEOUT`.
- Memory: Hobby 2 GB / 1 vCPU; Pro and Enterprise up to 4 GB / 2 vCPU.
- Request or response body: 4.5 MB maximum, otherwise 413 `FUNCTION_PAYLOAD_TOO_LARGE`.
- Bundle size: 250 MB uncompressed (500 MB for Python), enforced by AWS; large functions up to 5 GB are in beta. For Next.js use `outputFileTracingIncludes` rather than `includeFiles` and `excludeFiles`.
- Regions: a single region by default (iad1), changeable; Pro and Enterprise can set several.
- Cost is active CPU time plus provisioned memory time; waiting on I/O does not count as active CPU. Set a reasonable maximum duration.
- 1,024 file descriptors are shared across concurrent executions, including runtime usage.

## 4. Deployment Protection
- Methods: Vercel Authentication, Passport (Enterprise), Password Protection (Pro at $20 per month per protected project, Enterprise, not Hobby) and Trusted IPs (Enterprise).
- Scope: Standard Protection (recommended; all deployments except production domains), All Deployments, or production-only through Trusted IPs. It requires authentication for all requests, including to Routing Middleware.
- With Standard Protection the production generated deployment URL becomes restricted, so requests built from `VERCEL_URL` or `VERCEL_BRANCH_URL` should target the requested domain instead (relative paths client side; the request origin plus cookies server side). Protection Bypass for Automation exists for automation.

## Verify
- [ ] Preview deployments use their own environment values, and a deployed preview URL is checked before promoting.
- [ ] Function limits (duration, 4.5 MB body, memory, region) fit the workload.

## Checked
2026-11-09. Read the four cited Vercel pages in full. Removed (not on those pages): Root Directory and `turbo-ignore`, `vercel pull`/`build`/`--prebuilt`, `NEXT_PUBLIC_*` build-time inlining and system variable names, `waitUntil`, the region latency figure, edge-runtime guidance, CDN caching, `revalidatePath`, `x-vercel-cache`, Speed Insights and log drains, automatic TLS, spend management and image optimisation advice.
Method: documentation only; no commands were run.
