---
id: computing-software.game-programming.unity.ugui-pooled-scrollrect-virtual-lists
name: ugui-pooled-scrollrect-virtual-lists
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-ui, scrollrect-pooling, virtualized-list, ugui, game-programming]
level: practitioner
status: draft
description: "Build virtualised uGUI ScrollRect lists that pool item views for thousands of entries: index math, recycling on scroll, variable heights and layout pitfalls."
sources: ["https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/script-ScrollRect.html", "https://unity.com/how-to/unity-ui-optimization-tips"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pooled virtualised ScrollRect lists

**Goal:** inventory/leaderboard/chat lists with 10,000 rows that scroll at full frame rate.

## Why default ScrollRect fails
One GameObject per row with a VerticalLayoutGroup + ContentSizeFitter: every change dirties the
whole layout, canvas rebuild touches all rows, memory grows with rows.

## Fixed-height virtualisation
- Content height = `count * rowHeight + spacing`; set `content.sizeDelta` directly. **No layout group,
  no ContentSizeFitter** on content.
- Pool `visibleCount = ceil(viewportHeight / rowHeight) + 2` row views.
- On `scrollRect.onValueChanged`, compute first visible index and reposition/rebind:
```csharp
void OnScroll(Vector2 _) {
    float y = content.anchoredPosition.y;                    // top-anchored content, pivot (0.5,1)
    int first = Mathf.Clamp(Mathf.FloorToInt(y / rowHeight), 0, Mathf.Max(0, count - pool.Count));
    for (int i = 0; i < pool.Count; i++) {
        int index = first + i;
        var row = pool[i];
        bool show = index < count;
        row.gameObject.SetActive(show);           // or move off-screen to avoid OnEnable costs
        if (!show) continue;
        row.rect.anchoredPosition = new Vector2(0, -index * rowHeight);
        if (row.boundIndex != index) { row.Bind(data[index]); row.boundIndex = index; }
    }
}
```
Only rebind when the index changes; rebinding text every frame defeats the point.

## Variable heights
Precompute heights (measure with `TMP_Text.GetPreferredValues` off-screen once per item) and keep a
prefix-sum array; binary search for the first visible index.

## Canvas hygiene
- Put the list on its own nested Canvas so its rebuilds do not dirty the rest of the UI.
- Use a `RectMask2D` on the viewport (cheaper than Mask, culls children).
- Raycast Target off on non-interactive images and texts.

## Gotchas
- Gamepad navigation: pooled rows change identity; navigation targets must be rebuilt or handled by
  index.
- Inertia/elasticity overshoot can produce negative positions; clamp index.
- Data changes: call a `Refresh()` that resets `boundIndex = -1` on all rows.

## Verify
- [ ] Profiler: `Canvas.BuildBatch`/layout cost constant regardless of item count.
- [ ] Fling-scroll 10k rows: no GC spikes (no Instantiate during scroll).
