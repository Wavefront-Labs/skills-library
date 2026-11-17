---
id: creative-arts.animation.pipeline.kitsu-and-gazu
name: kitsu-and-gazu
category: creative-arts
field: animation
product: pipeline
tags: [kitsu, gazu, zou, cgwire, production-tracking, open-source, python-client]
level: practitioner
status: draft
description: "Track an animation production with Kitsu (CGWire): Zou API, Gazu Python client, self-hosting, entities and task statuses, and scripting examples."
sources:
  - https://www.cg-wire.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Kitsu and Gazu

**Kitsu** is an open-source (with hosted options) production tracker from CGWire built for animation and VFX studios. It tracks projects, episodes, sequences, shots, assets, tasks, statuses, previews and playlists. **Zou** is its API server, and **Gazu** is the official Python client.

## Components
- **Kitsu**: the web front end.
- **Zou**: the REST API and database layer.
- **Gazu**: `pip install gazu`.
- Run it yourself (the project documents a Docker-based installation) or use the hosted service; check the CGWire documentation for the current instructions.

## Gazu basics
```python
import gazu
gazu.set_host("https://kitsu.example.com/api")
gazu.log_in("user@example.com", "password")     # use an API/service account

project = gazu.project.get_project_by_name("MyShow")
for shot in gazu.shot.all_shots_for_project(project):
    print(shot["name"])

tasks = gazu.task.all_tasks_for_shot(shot)
```
Typical operations include creating assets and shots (`gazu.asset.new_asset(...)`, `gazu.shot.new_shot(...)`), listing tasks, changing task status, and publishing previews and comments. Function names evolve between versions; use the Gazu documentation as the reference.

## Habits
- Use a **dedicated service account** for scripts, and read credentials from environment variables.
- Set up **task types** (storyboard, layout, animation, lighting, compositing) and **task statuses** to match your pipeline before adding assets and shots.
- Keep **frame ranges and fps** on shots (as metadata) so it can drive editorial and render tools.
- Use **playlists** for dailies review (`review-playlists-and-dailies.md`).
- Compare with ShotGrid (`shotgrid-python-api.md`): Kitsu is lighter and animation-focused; ShotGrid has deeper integrations and Toolkit.

## Verify
- [ ] Script account has the right role and no shared credentials in code.
- [ ] Task types and statuses match the pipeline vocabulary.
- [ ] A script run creates entities once, without duplicates.
