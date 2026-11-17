---
id: creative-arts.animation.pipeline.shotgrid-python-api
name: shotgrid-python-api
category: creative-arts
field: animation
product: pipeline
tags: [shotgun-api3, shotgrid, flow-production-tracking, python-api, production-tracking, find-create-update]
level: advanced
status: draft
description: "Script ShotGrid (Flow Production Tracking) with shotgun_api3: authentication, find with filters and fields, create, update, batch, pagination, upload, rate-limit hygiene."
sources:
  - https://developer.shotgridsoftware.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ShotGrid Python API (shotgun_api3)

Autodesk's ShotGrid, rebranded Flow Production Tracking, is exposed to Python through the `shotgun_api3` module (the module name has not changed). Docs are at developer.shotgridsoftware.com.

## Connect
```python
import os, shotgun_api3
sg = shotgun_api3.Shotgun(
    "https://yoursite.shotgrid.autodesk.com",
    script_name="pipeline_script",
    api_key=os.environ["SG_SCRIPT_KEY"],
)
```
- Use a **script key** (created by an admin in the site's Scripts page) for automation, with the minimum permission role. For user actions, use user login with session tokens and keep passwords out of code.
- Read the key from the environment or a secrets store; never commit it.

## Core calls
```python
proj = {"type": "Project", "id": 123}
shots = sg.find("Shot",
    [["project", "is", proj], ["sg_status_list", "is_not", "omt"]],
    ["code", "sg_status_list", "sg_cut_in", "sg_cut_out"],
    order=[{"field_name": "code", "direction": "asc"}], limit=0)

new = sg.create("Shot", {"project": proj, "code": "EP01_010", "sg_status_list": "wtg"})
sg.update("Shot", new["id"], {"description": "Opening wide"})
one = sg.find_one("Shot", [["id", "is", new["id"]]], ["code"])
```
- Filters are `[field, operator, value]` triples; entity values are `{"type": ..., "id": ...}` dicts. Custom fields start with `sg_`.
- `limit=0` means all results (with paging done by the library); also available are `page`, `retired_only` and `include_archived_projects`.
- `sg.batch([...])` sends many create/update/delete requests in one transaction, which is far faster than loops.
- `sg.upload("Version", id, path, field_name="sg_uploaded_movie")` attaches media. `sg.upload_thumbnail` for thumbnails.
- `sg.schema_field_read("Shot")` lists fields, for discovering names.

## Habits
- Request only the fields you need; avoid per-entity calls in loops.
- Keep a retry with back-off around calls; the server can throttle.
- Test against a **sandbox site** before touching production data.
- Wrap field names and statuses in constants; status codes are short strings (such as `wtg`, `ip`, `fin`) configured per site.

## Verify
- [ ] The script key has minimal role permissions.
- [ ] A dry run on a sandbox returns the expected entities.
- [ ] Batch calls are used for bulk writes.
