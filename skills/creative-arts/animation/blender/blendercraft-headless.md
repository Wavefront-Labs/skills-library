---
id: creative-arts.animation.blender.blendercraft-headless
name: blendercraft-headless
category: creative-arts
field: animation
product: blender
tags: [blender, bpy, headless, cli, scripting, python, automation, reproducible]
level: advanced
status: verified
description: "Run Blender fully headless via bpy: blender -b --python with argv, open-set-append-cast scene builds, abspath output, deterministic shot rebuilds."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SKILL: blendercraft — headless Blender automation

**Why:** every shot must be scriptable and reproducible — no GUI clicking — so shots are
deterministic across episodes and seasons, and so a single machine can grind an entire
15-minute episode shot by shot. This is the verified pattern behind
`series/production/blender/render_shot.py`.

## 1. The invocation

```bash
blender -b --python render_shot.py -- <EPID> <SHOT_ID> <OUTDIR> [rhubarb.json]
```
- `-b` / `--background` — no UI, no window; exits when the script returns.
- `--python script.py` — run our builder in Blender's embedded Python.
- Everything after the bare `--` is **ours**, invisible to Blender. Read it with:
  ```python
  argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
  EPID, SHOT_ID, OUTDIR = argv[0], argv[1], os.path.abspath(argv[2])
  RHUBARB = argv[3] if len(argv) > 3 else None
  ```
  The `if '--' in sys.argv` guard keeps the script importable/runnable in the GUI too.
- **Write scripts to `.py` files** (Write tool), never heredoc Python into the shell —
  EOF/quote escaping silently corrupts multi-line Python. Lesson already paid.
- To add our own shared modules, `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`
  then `import shotkit` — Blender's embedded Python won't find a sibling module otherwise.

## 2. Scene build pattern: open set → append cast → stage → render

The verified build is **not** factory-reset-and-model. It **opens a locked set .blend**
and **appends locked character .blends** onto staging marks. Assets are authored once and
reused forever — that is the consistency guarantee.

```python
bpy.ops.wm.open_mainfile(filepath=SET_MAP[loc])   # locked set is the scene
scene = bpy.context.scene
```

**Appending a character** (link=False = make a local copy that travels with the shot):
```python
def append_char(path):
    before = set(bpy.data.objects)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = list(src.objects)                  # pull ALL objects from the asset
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:                                        # append does NOT auto-link to scene
        if o.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(o)
    root  = next((o for o in new if o.type=='EMPTY' and o.name.startswith('TURN')), None)
    mouth = next((o for o in new if o.name.startswith('mouth')), None)
    return root, new, mouth
```
Key gotchas baked into that function:
- `libraries.load(..., link=False)` **appends** (local copy, editable, self-contained
  render). `link=True` **links** (shared, read-only, lighter) — use link only for a set
  dressed into many shots where you never deform it; use append for anything you animate.
- Appended objects are **not** linked into the active scene collection automatically —
  you must `collection.objects.link(o)` each one or it renders invisibly absent.
- Diff `set(bpy.data.objects)` **before/after** to find exactly what the append brought
  in (names collide/get `.001` suffixes otherwise).
- Find the rig's control **root** and **mouth** by name convention (a `TURN*` empty, a
  `mouth*` mesh) so downstream staging/lip-sync has stable handles.

## 3. Deterministic staging from data

Stage cast on **locked marks** per location: `name -> (x, y, face_deg, head_z)`. The
builder places `root.location = (x, y, 0)` and a clamped facing rotation, then reads the
shot's `size` to derive the camera (see `camera-cinematography.md`). Shot spec is **JSON**
(`<EPID>_shotlist.json`): size, cast, duration, camera hint, line_id. Builder reads JSON →
identical shot every run. Regenerating a shot is just re-running the command.

## 4. The output-path bug (os.path.abspath or lose your frames)

Blender resolves a **relative `render.filepath` against the opened .blend's directory,
NOT the current working directory**. A relative out path can print `Saved`/`DONE` and
exit 0 while writing frames into the asset folder — nowhere you're looking. Always:
```python
OUTDIR = os.path.abspath(argv[2])
...
scene.render.filepath = os.path.join(os.path.abspath(outdir), "f_")
os.makedirs(outdir, exist_ok=True)
```
This bit the first render. `shotkit.cinematic_render()` now does the abspath internally.
The same trap applies to sim/VDB cache directories (see `smoke-fire-fx.md`).

## 5. Fail loud, log, chunk, skip-gate

- **Asset gate:** before building, check every set/char in the shot exists in the asset
  map. If not, **print `SKIP <id>: missing assets ... -> BUILD QUEUE` and return** — don't
  render a broken shot, log it for the build queue instead. Likewise skip non-3D sizes
  (`FX`/`TITLE`) that a comp pass owns.
- **Log every step** (`print`) — set loaded, cast appended, lip-sync applied, frames
  rendered. A headless run leaves only stdout; a silent failure is undebuggable.
- **One shot per process.** Render shots as separate `blender -b` invocations, not one
  monster scene. Each is recoverable, parallelisable, and can't leak state into the next.
  Running many shots = a loop over the shotlist firing one command each (optionally
  several in parallel up to VRAM).
- **Clean slate guarantee:** because each shot opens a fresh set file in a fresh process,
  there is no state bleed — the determinism comes from the process boundary, not from
  resetting inside a long-lived session.

## 6. bpy fundamentals for batch

- `bpy.ops.*` act on context; in background mode context can be thin — prefer data-level
  edits (`bpy.data`, object properties) over ops where possible, and set
  `scene`/`view_layer` explicitly.
- `bpy.context.view_layer.update()` before reading a freshly-moved object's
  `matrix_world` (e.g. to parent the lip-sync oval to the mouth's world position).
- Keyframe via `obj.keyframe_insert('location', frame=f)`; fix interpolation by walking
  `obj.animation_data.action.fcurves[*].keyframe_points`.

## 7. Running many shots

A whole episode is a loop over the shotlist, one process per shot:
```bash
for sid in $(python -c "import json,sys; sl=json.load(open('EP01_shotlist.json')); \
  print('\n'.join(s['id'] for sq in sl['sequences'] for s in sq['shots']))"); do
    blender -b --python render_shot.py -- EP01 "$sid" "workspace/renders/EP01/$sid" \
      || echo "FAIL $sid" >> workspace/renders/EP01/failures.log
done
```
- Each shot is a **clean process** — no state bleed, a crash kills one shot not the batch,
  and failures are logged for a single retry pass (see `rendering-amd-hip.md`).
- The builder itself decides per shot whether to render, skip-gate a missing asset, or
  hand a non-3D size to comp — so the loop is dumb and the script is smart.
- To parallelise, fan out a few processes at once up to VRAM headroom; cel shots are light
  enough that 2-3 concurrent on the 16 GB card is usually safe.

## In this pipeline

`series/production/blender/render_shot.py` is the reference builder: argv after `--`,
`open_mainfile` the set, `append_char` with the before/after object diff and explicit
collection linking, data-driven marks + camera recipe, optional Rhubarb lip-sync on the
primary speaker, then `shotkit.cinematic_render()` which abspaths the output. `shotkit.py`
holds the shared beauty/render finish so every shot ends at the same tier.

## Verify

1. **Args:** run with missing args → clean failure, not a stack trace mid-build.
2. **Append:** the appended character is visible in the render (linked into the scene
   collection), rig root + mouth handles found.
3. **Output lands:** frames appear in the **abspath** OUTDIR, not beside the .blend;
   `DONE` with zero frames on disk means the relative-path bug.
4. **Skip-gate:** a shot referencing an unbuilt asset prints `SKIP ... BUILD QUEUE` and
   renders nothing.
5. **Determinism:** run the same shot twice from clean processes → identical frames.

See also: `rendering-amd-hip.md`, `camera-cinematography.md`, `lip-sync.md`,
`../pipeline/shot-episode-structure.md`.
