---
id: computing-software.software-engineering.mobile-development.flash-list-and-list-performance
name: flash-list-and-list-performance
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, flashlist, flash-list, flatlist, list-performance, recycling, virtualized-list, userecyclingstate, masonry, numcolumns, list-virtualization, onblankarea, getitemtype, mobile-lists, scroll-performance]
level: advanced
status: docs-checked
description: "Render long React Native lists with FlashList v2: recycling and the state-reset rules for item components, FlatList props not implemented, masonry, and blank-cell debugging."
sources: ["https://shopify.github.io/flash-list/docs/", "https://shopify.github.io/flash-list/docs/usage/", "https://shopify.github.io/flash-list/docs/known-issues"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FlashList: recycling list rendering

**Goal:** render long lists without FlatList's blank cells and frame drops, by using FlashList's
cell recycling and writing item components that survive being recycled.

FlashList is Shopify's list that keeps a recycle pool: items cached in the pool when they scroll off
the screen are reused, and setting `maxItemsInRecyclePool` to `0` disables the pool so items unmount
once scrolled off. The Usage page says "If you are familiar with FlatList, you already know how to
use FlashList", and the FlashList docs are split by version (v1 docs for old architecture are
selected from a version dropdown).

```tsx
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={({ item }) => <Row item={item} />}
  keyExtractor={item => item.id}
/>
```

## v2 notes
- `overrideItemLayout` supports `span`, and the docs say size estimates "are no longer needed or
  read" in v2. FlashList does not render items in the first cycle: items are drawn after it
  measures itself at the end of the first render, and `onLoad` reports `elapsedTimeInMs`.
- Memoizing props passed to FlashList is "more important in v2"; v1 was more selective about
  updating items. A valid `keyExtractor` is highly recommended with v2.
- Masonry is the `masonry` prop (use with `numColumns` greater than 1).
- These FlatList props are not implemented and "We don't currently plan to implement" them:
  `disableVirtualization`, `getItemLayout`, `initialNumToRender`, `maxToRenderPerBatch`,
  `recordInteraction`, `setNativeProps`, `updateCellsBatchingPeriod`, `onScrollToIndexFailed`,
  `windowSize`. Also not implemented: `columnWrapperStyle`, `debug`, `listKey`.

Confirm the installed major version before copying any snippet.

## The migration checklist from the docs
- Scan the `renderItem` hierarchy for explicit `key` props and remove them. For `.map()` use the
  `useMappingHelper` hook, whose `getMappingKey` takes an index and an item key.
- Check `renderItem` components that use `useState` and verify whether that state must reset when a
  different item is passed to the component.
- Pass types via `getItemType` for heterogeneous lists "to improve performance" so the right type
  is used for the right item. Default type is `0`; return `undefined` to keep the default for an
  index. The method is called very frequently, so keep it fast. `overrideItemLayout` is also called
  very frequently.
- Do not test performance with JS dev mode on; use release mode, because FlashList "can appear
  slower while in dev mode due to a small render buffer".
- Nesting horizontal FlashLists in vertical lists: make the vertical list a FlashList too.

```tsx
import { useRecyclingState } from '@shopify/flash-list';

function Row({ item }) {
  // state resets without an extra setState when the dependencies change
  const [expanded, setExpanded] = useRecyclingState(false, [item.id], () => {
    // optional reset callback, e.g. reset scroll positions of nested horizontal lists
  });
}
```
- `useRecyclingState(initialState, dependencies, resetCallback)` is like `useState` with a
  dependency array and includes the behaviour of `useLayoutState`.
- `useLayoutState` is like `useState` but communicates the change to FlashList. It is useful when
  resizing a child based on local state; without it layout changes are still detected via
  `onLayout`, which "might not look as smooth".
- `prepareForLayoutAnimationRender()` disables recycling for the next frame so layout animations
  run well. Avoid it with large data changes: single insertions or deletions should animate
  smoothly. `keyExtractor` is also needed for layout animations.

## Props worth knowing
Documented props include `renderItem`, `data`, `horizontal`, `numColumns`, `inverted`,
`initialScrollIndex`, `keyExtractor`, `onEndReached` / `onEndReachedThreshold`, `onStartReached` /
`onStartReachedThreshold`, `onRefresh`, `refreshing`, `refreshControl` (overrides the built-in one
and makes `onRefresh` and `refreshing` ignored), `ItemSeparatorComponent`,
`ListHeaderComponent` / `ListFooterComponent` / `ListEmptyComponent`, `contentContainerStyle`,
`extraData`, `onViewableItemsChanged`, `viewabilityConfig`, `maintainVisibleContentPosition`,
`CellRendererComponent`, `drawDistance`, `getItemType`, `masonry`, `maxItemsInRecyclePool`,
`onLoad`, `onBlankArea`, `overrideItemLayout`, `optimizeItemArrangement`, `onChangeStickyIndex` and
`stickyHeaderConfig` (its examples also use `stickyHeaderIndices`). FlashList uses `ScrollView`
under the hood, so ScrollView props apply.

## Layout and style rules
- `style` is for the FlashList's parent container. The docs "highly" recommend avoiding padding on
  it, because FlashList assumes the parent view and the ScrollView are the same size; use
  `contentContainerStyle`, which accepts `backgroundColor` and padding properties only.
- `numColumns` renders multiple columns only with `horizontal={false}`, zig-zagging like a
  `flexWrap` layout; items should all be the same height. For varying heights use `masonry`.
  `optimizeItemArrangement` (default true) tries to reduce differences in column height by
  changing item order, with masonry.
- `overrideItemLayout` can set `layout.span` so some items are bigger in a grid.
- `maintainVisibleContentPosition` is enabled by default; known issue 3 says data re-ordering can
  cause items to move, and you can disable it with `maintainVisibleContentPosition={{disabled:true}}`.
- Horizontal list with a fixed size or a header: FlashList assumes the list height is fixed; the
  known-issues page suggests rendering the header as the first item with its own `getItemType`.

## Diagnosing blank cells and jank
- `onBlankArea` reports `offsetStart`, `offsetEnd` and `blankArea` (the max of the two; negative
  values mean items render outside the visible area). It fires even for expected blanks, such as
  too few items to fill the screen, and works from native `onDraw` (Android) and `layoutSubviews`
  (iOS), not the JS `onScroll` event.
- `onLoad` is not fired if `ListEmptyComponent` is rendered.
- `viewabilityConfig` cannot be changed on the fly. Viewability callbacks may be deferred until the
  JS thread is less busy; use the `timestamp` on the `ViewToken`. `minimumViewTime` defaults to
  250 ms and the docs do not recommend much lower values.
- `onCommitLayoutEffect` is called before layout is committed; `setState` inside it can lead to
  infinite loops, so memoize FlashList's props.
- `inverted` uses `scaleY(-1)` on iOS and web and `rotate(180deg)` on Android, so on Android the
  scrollbar appears on the left.
- Horizontal lists with RTL layouts: FlashList cannot read the padding applied via
  `contentContainerStyle`; for precise `scrollTo` or `initialScrollIndex`, pad the header instead.

## Verify
- [ ] The installed major version matches the docs being followed.
- [ ] Scroll a list of varied items in release mode on a real device and watch `onBlankArea`.
- [ ] Expand a row, scroll away, scroll back: state tied to the previous item is reset.
- [ ] Heterogeneous lists set `getItemType`.
- [ ] No padding on the FlashList's `style`.

## Checked
2026-11-08. Confirmed against the FlashList Usage page (last updated 2026-10-01), Introduction and
Known issues pages: migration steps, prop descriptions and defaults, hooks, methods, unsupported
FlatList props, `onBlankArea`, `onLoad`, `inverted` and viewability notes. Removed because the pages
do not state them: the `estimatedItemSize` v1 requirement, the `MasonryFlashList` rename, "recycled
components keep their refs", details of `useMappingHelper` argument order (the page text and
example disagree, so only the parameter names are kept), and the failure-mode list. The FlatList
page source was dropped because no claim depends on it.
Method: documentation only; no commands were run.
