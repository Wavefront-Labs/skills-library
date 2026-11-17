---
id: computing-software.cloud-infrastructure-engineering.docker.base-image-eol-and-distro-lifecycle-planning
name: base-image-eol-and-distro-lifecycle-planning
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, base-image, base-image-eol, distro-lifecycle, debian-codenames, ubuntu-lts, alpine-branches, end-of-life, upgrade-planning, endoflife-date]
level: practitioner
description: "Plan base image upgrades around OS lifecycles: Debian security and LTS windows, Alpine branch support, pinned codenames."
sources: ["https://endoflife.date/", "https://wiki.debian.org/DebianReleases", "https://alpinelinux.org/releases/", "https://github.com/docker-library/official-images#library-definition-files", "https://ubuntu.com/about/release-cycle"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Base image EOL and lifecycle planning

**Goal:** know when each base stops getting security fixes and schedule the move *before*
that date, because an EOL base can show few scanner findings for new CVEs, not because it
is safe but because nobody is tracking it.

## Lifecycles that matter
| Base | What the vendor page says |
|---|---|
| Debian (`bookworm`, `trixie`) | Debian security team supports a stable release for three years (its whole life plus about a year after the next stable). Total lifetime from release to end of security updates is 5 years: three years of full support then two years of Long Term Support (LTS) |
| Alpine (`3.x` branches) | The `main` repository is typically supported for 2 years per branch (its release page gives each branch's dates) |
| Ubuntu LTS | See the Ubuntu release cycle page for standard and Ubuntu Pro support windows (the page renders its dates dynamically) |
| Language images (`python:3.12`) | Follow the upstream project's end-of-life; look the dates up per product |

`endoflife.date` lists end-of-life dates per product and cycle for the distros and runtimes above.
The Docker Official Images repository defines which tags are built (library definition files);
check it for the codenames and versions still being built before choosing a tag.

## A workable policy
1. **Pin the codename** in tags (`python:3.12-slim-bookworm`, not `3.12-slim`) so a Debian
   release does not silently rebase you, then upgrade the codename deliberately.
2. **Set a reminder at EOL minus 6 months** for every distinct base in the fleet. A
   scheduled CI job that reads `FROM` lines and compares each codename or version with its
   endoflife.date entry works and costs nothing.
3. **Upgrade the language image first, then the OS**, for example `python:3.11-slim-bookworm` ->
   `3.12-slim-bookworm` -> `3.12-slim-trixie`, with a test run between.
4. **Keep an inventory**: `docker images --format '{{.Repository}}:{{.Tag}}'` across hosts, or
   list tags registry-side.

## Signs you are on an EOL base
- Package updates stop arriving, or `apt-get update` fails against the distribution's security
  archive after the suite reaches end of life.
- Your scanner reports the OS as unsupported or stops reporting new findings; treat that as a
  warning, not as a clean result.

## Gotchas
- Unpinned tags such as `latest` move when the distribution publishes a new release; pin a
  codename and, in production, a digest.
- Check a runtime's own release schedule (for example Node's) before basing production on a short-lived release line.

## Verify
For each `FROM` in the repo, the base's cycle shows a future end-of-life date on endoflife.date, and the scanner recognises the OS as supported.

## Checked
2026-11-09. Confirmed against the Debian releases wiki (three-year security support; 5-year total with two years of LTS) and the Alpine releases page (main repository typically supported for 2 years).
Removed as unconfirmed or JavaScript-only in the fetched pages: the Debian "every ~2 years" and Ubuntu "April of even years", 5 and 10 year Ubuntu figures, Alpine "every 6 months", Distroless and Wolfi rows, Python/Node/Go lifetime figures, the claim that official images stop rebuilding at Debian regular-support EOL, the endoflife.date API URL, the Trivy message text and `apk` error strings, the buildx base-image annotation claim, and the `latest` tag behaviours.
Method: documentation only; no commands were run.
