---
id: computing-software.software-engineering.v-lang.v-gg-graphics
name: v-gg-graphics
category: computing-software
field: software-engineering
product: v-lang
tags: [v-gg-graphics, terminal-gui-modules, gg, graphics, sokol, 2d, game, window, draw_rect, frame_fn, opengl, image, v-lang]
level: advanced
status: draft
description: "Open a window with gg.new_context, handle frame, event and init callbacks, draw shapes, text and images, and play with sokol."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# gg: 2D graphics and games

Goal: draw windows with the built-in gg library.

```v
import gg
struct App { mut: ctx &gg.Context = unsafe { nil } }
fn frame(mut a App) {
    a.ctx.begin()
    a.ctx.draw_rect_filled(10, 10, 100, 50, gg.red)
    a.ctx.draw_text(20, 20, 'hi', size: 20)
    a.ctx.end()
}
fn main() {
    mut a := &App{}
    a.ctx = gg.new_context(width: 640, height: 480, window_title: 'demo', user_data: a, frame_fn: frame)
    a.ctx.run()
}
```
- Callbacks: `init_fn`, `frame_fn`, `event_fn` (keyboard/mouse), `click_fn`, `keydown_fn`.
- Images: `ctx.create_image(path)!`, `ctx.draw_image(x, y, w, h, img)`; fonts via `font_path`.
- Built on sokol (OpenGL/Metal/D3D11); requires graphics libs on Linux (`libx11`, `libgl`; confirm packages).
- Games/examples: `v/examples/gg`, `tetris`, `2048`.

Gotchas:
- Use `a.ctx.begin()/end()` each frame.
- Resources must be created after `init_fn`.
- API is still changing; confirm against your V version.

Verify: window opens and draws the rectangle.
