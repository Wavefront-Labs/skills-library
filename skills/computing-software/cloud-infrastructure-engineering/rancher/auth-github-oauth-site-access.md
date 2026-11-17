---
id: computing-software.cloud-infrastructure-engineering.rancher.auth-github-oauth-site-access
name: auth-github-oauth-site-access
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [github, oauth, authorized-users, site-access, client-id, external-principal]
level: intro
status: docs-checked
description: "Enable GitHub sign-in for Rancher: create the OAuth app, paste Client ID and Secret, and pick a Site Access mode that does not let any GitHub user in."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/authentication-config/configure-github
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sign in to Rancher as a local user with the `administrator` role (the local principal), then go to **Users & Authentication > Auth Provider > GitHub**. Follow the on-screen directions to set up a GitHub application; Rancher redirects you to GitHub to register it. The Authorization Callback URL is where users re-enter Rancher after GitHub authenticates them.

Copy the **Client ID** and **Client Secret** from GitHub (Settings > Developer Settings > OAuth Apps) into Rancher, then click **Authenticate with GitHub**.

Choose a **Site Access** option:

- **Allow any valid Users**: any GitHub user can reach Rancher. The page generally discourages this.
- **Allow members of Clusters, Projects, plus Authorized Users and Organizations**: any GitHub user or group added as a Cluster Member or Project Member can log in, as can anyone on the Authorized Users and Organizations list.
- **Restrict access to only Authorized Users and Organizations**: only those listed can log in.

Click **Enable**. Afterwards you are signed in with your GitHub account, which is the external principal.

The page tells you to read the External Authentication Configuration and Principal Users section first.

## Checked

2026-11-09. Read in full the Rancher Manager Configure GitHub page (authentication-config/configure-github). Every claim matched; nothing removed.

Method: documentation only; no commands were run.
