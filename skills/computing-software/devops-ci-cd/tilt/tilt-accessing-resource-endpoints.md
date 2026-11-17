---
id: computing-software.devops-ci-cd.tilt.tilt-accessing-resource-endpoints
name: tilt-accessing-resource-endpoints
category: computing-software
field: devops-ci-cd
product: tilt
tags: [accessing-resource-endpoints, tilt]
level: practitioner
status: docs-checked
description: "Expose links to services in the Tilt UI with static links, k8s_resource port_forwards, named port forwards, kubefwd, and ngrok tunnels."
sources:
  - "https://docs.tilt.dev/accessing_resource_endpoints.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Links and port forwards to your services

Goal: show a link on every Tilt dashboard to each running service, with Tilt handling the plumbing.

## Static links

Any resource accepts `links`. Supported for `local_resource`, `k8s_resource`, and `dc_resource`.

```
k8s_resource(
   workload='blog-site',
   links=[
      'blog-db.storage.acme.com',
      link('internal-eng.acme.com/docs/blog-db-reset', 'Blog db reset docs')
   ]
)
```

Links show on the main dashboard and the individual resource page.

## kubectl port-forward

```
k8s_resource(workload='blog-site', port_forwards=4002)
```

`localhost:4002` connects to container port 4002, and Tilt shows a link at the top of the screen automatically. With `port_forwards='9000:4002'`, `localhost:9000` connects to container port 4002.

## Multiple and named forwards

```
k8s_resource(
   workload='blog-site',
   port_forwards=[
      port_forward(9000, 4002, name='blog-hero-post'),
      port_forward(9001, 4003, name='blog-archives')
   ]
)
```

Custom names are displayed instead of `localhost:<port-forward>`.

## Bulk forwards with kubefwd

The `kubefwd` operator creates port-forwards for every service in the namespace you deploy to:

```
v1alpha1.extension_repo(name='default', url='https://github.com/tilt-dev/tilt-extensions')
v1alpha1.extension(name='kubefwd:config', repo_name='default', repo_path='kubefwd')
```

Downside: Tilt needs to prompt for `sudo` privileges because it changes DNS on your local machine.

## Public tunnels

Tilt has an `ngrok` operator that adds UI buttons to start/stop a public tunnel when needed; see the ngrok extension README.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/accessing_resource_endpoints.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
