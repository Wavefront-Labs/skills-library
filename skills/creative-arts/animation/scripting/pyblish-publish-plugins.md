---
id: creative-arts.animation.scripting.pyblish-publish-plugins
name: pyblish-publish-plugins
category: creative-arts
field: animation
product: scripting
tags: [pyblish, pipeline-python, dcc-python, publish-validation, collector, validator, extractor, integrator, ayon, openpype, python]
level: advanced
status: draft
description: "Write Pyblish publish plugins for DCC pipelines: collect/validate/extract/integrate order, instances and families, repair actions, and running headless."
sources:
  - https://pyblish.com/
  - https://api.pyblish.com/
  - https://github.com/pyblish/pyblish-base
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pyblish publish plugins

**Goal:** a publish step that refuses bad data (wrong names, missing UVs, unfrozen transforms, wrong
frame range) before it reaches the next department, the same way in every DCC. Pyblish is the
framework that OpenPype/Ayon publishing is built on.

## The four stages (CVEI)

| Order constant | Stage | Does |
|---|---|---|
| `CollectorOrder` (0) | Collect | find what to publish, create `instances` with data |
| `ValidatorOrder` (1) | Validate | check instances; raise to fail |
| `ExtractorOrder` (2) | Extract | write files to a staging dir |
| `IntegratorOrder` (3) | Integrate | move to final versioned location, register in database |

If any validator fails, extraction does not run.

## Minimal plugins

```python
import pyblish.api

class CollectModels(pyblish.api.ContextPlugin):
    order = pyblish.api.CollectorOrder
    hosts = ["maya"]
    def process(self, context):
        from maya import cmds
        for grp in cmds.ls("*_GRP", type="transform"):
            inst = context.create_instance(grp, family="model")
            inst[:] = cmds.listRelatives(grp, allDescendents=True, fullPath=True) or []

class ValidateNoNgons(pyblish.api.InstancePlugin):
    order = pyblish.api.ValidatorOrder
    families = ["model"]
    label = "No n-gons"
    def process(self, instance):
        from maya import cmds
        bad = []
        for mesh in cmds.ls(instance, type="mesh", long=True):
            # polyInfo lines look like "FACE   0:   0   1   3   2"
            for line in cmds.polyInfo(mesh, faceToVertex=True) or []:
                if len(line.split(":")[1].split()) > 4:
                    bad.append(mesh)
                    break
        if bad:
            raise ValueError("N-gons on: %s" % bad)
```

Register and run:
```python
import pyblish.api, pyblish.util
pyblish.api.register_host("maya")
pyblish.api.register_plugin_path("<PIPELINE>/plugins/publish")
ctx = pyblish.util.publish()
errors = [r["error"] for r in ctx.data["results"] if r["error"]]
```
GUI: `pyblish_qml` or `pyblish_lite` show results with per-plugin pass/fail.

## Repair actions

```python
class SelectInvalid(pyblish.api.Action):
    label = "Select invalid"; on = "failed"
    def process(self, context, plugin): ...
```
Attach with `actions = [SelectInvalid]`; artists fix with one click.

## Gotchas

- Plugins filter by `families` and `hosts`; a typo silently skips the plugin. Log which plugins ran.
- Keep validators fast and side-effect free; extractors are where files are written.
- Use `optional = True` for validators artists may skip, and record that they skipped.

## Verify

A deliberately broken scene fails the right validator with a readable message; a clean scene publishes
and the integrator writes the expected versioned path.
