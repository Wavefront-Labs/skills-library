---
id: computing-software.systems-network-administration.varnish-cache.docker-container-deploy
name: docker-container-deploy
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [docker, container, varnish-size, docker-run]
level: practitioner
status: docs-checked
description: "Run Varnish from the official Docker image: mount a VCL file, tmpfs for the working directory, VARNISH_SIZE for the cache size, and extra varnishd parameters after the image name."
sources:
  - https://www.varnish.org/docs/install-guide/install-docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# docker container deploy

```bash
docker pull varnish          # or pin a tag, e.g. varnish:8.0
docker run -v /path/to/default.vcl:/etc/varnish/default.vcl:ro \
  --tmpfs /var/lib/varnish:exec \
  --name varnish \
  -p 80:80 \
  -e VARNISH_SIZE=2G \
  varnish
```

- Mount the VCL read-only (`:ro`) at `/etc/varnish/default.vcl`.
- `--tmpfs /var/lib/varnish:exec` keeps the frequently accessed working directory in memory; `:exec` allows execution.
- The default cache size is 100 MB; `VARNISH_SIZE` overrides it.
- Anything after the image name is passed to varnishd, so `docker run varnish -p default_ttl=3600` sets the default TTL to one hour (default is 2 minutes).

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the varnishtest-in-container command and the Verify tip.

Method: documentation only; no commands were run.
