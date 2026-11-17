---
id: computing-software.software-engineering.textual.textual-tree-widgets
name: textual-tree-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-trees, tree, directory-tree, filter-paths, tree-node, tui]
level: practitioner
status: docs-checked
description: "Build a Textual Tree with TreeNode add and add_leaf, handle node messages, and filter a DirectoryTree by overriding filter_paths."
sources: [https://textual.textualize.io/widgets/tree/, https://textual.textualize.io/widgets/directory_tree/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual Tree and DirectoryTree

Goal: show hierarchical data or the filesystem.

## Method
**Tree** (0.6.0+): the widget has a `root` attribute, a `TreeNode`. Call `add()` or `add_leaf()` on a node to add children underneath it; both return the child `TreeNode`, so you can nest further.
- Reactives: `show_root` (True), `show_guides` (True), `guide_depth` (4, indentation between parent and child).
- Messages: `Tree.NodeCollapsed`, `Tree.NodeExpanded`, `Tree.NodeHighlighted`, `Tree.NodeSelected`.

**DirectoryTree**: a tree to navigate the filesystem, created from a path (the docs example opens the current working directory). It has the same reactives and inherits the Tree bindings.
- Messages: `DirectoryTree.FileSelected` and `DirectoryTree.DirectorySelected`, each with `node` and `path`. `reload()` refreshes the contents; setting `path` repopulates the tree from the new root.
- Filtering: subclass `DirectoryTree` and implement `filter_paths`, which takes an iterable of `Path` objects and returns those that pass. The docs example filters out hidden files and directories:

```python
class FilteredDirectoryTree(DirectoryTree):
    def filter_paths(self, paths):
        return [path for path in paths if not path.name.startswith(".")]
```

## Checked
2026-11-07. Read in full: Tree and DirectoryTree widget pages. Confirmed: 0.6.0 badge, root TreeNode with add/add_leaf returning the child, show_root/show_guides/guide_depth defaults, four Tree messages, DirectoryTree path argument, inherited bindings, FileSelected, filter_paths override example. Added: DirectorySelected, reload and path watch from the page. Removed: the Verify section.
Method: documentation only; no commands were run.
