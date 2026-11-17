---
id: computing-software.software-engineering.objective-c.uitableview-datasource
name: uitableview-datasource
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-ui, uitableview-datasource]
level: practitioner
status: draft
description: "Implement UITableViewDataSource and delegate methods with cell reuse, diffing via batch updates or diffable data sources."
sources:
  - https://developer.apple.com/documentation/uikit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UITableView data source
**Goal:** a correct, efficient list.

```objc
- (NSInteger)tableView:(UITableView *)tv numberOfRowsInSection:(NSInteger)s { return self.items.count; }
- (UITableViewCell *)tableView:(UITableView *)tv cellForRowAtIndexPath:(NSIndexPath *)ip {
    UITableViewCell *cell = [tv dequeueReusableCellWithIdentifier:@"Cell" forIndexPath:ip];
    cell.textLabel.text = self.items[ip.row].title;
    return cell;
}
// setup
[self.tableView registerClass:[UITableViewCell class] forCellReuseIdentifier:@"Cell"];
```
- Required: `numberOfRowsInSection:` and `cellForRowAtIndexPath:`; optional `numberOfSectionsInTableView:`.
- Always dequeue; reset all cell state in `prepareForReuse` and in the data-source method (reused cells carry stale content).
- Updates: wrap in `performBatchUpdates:completion:` with matching data model changes or reload; mismatch raises an exception ("number of rows ... must be equal").
- Modern alternative: `UITableViewDiffableDataSource` with snapshots.
- Self-sizing cells: `tableView.rowHeight = UITableViewAutomaticDimension` plus `estimatedRowHeight` and Auto Layout in the cell.
- Do slow work (image decode, formatting) off the main thread and set results only if the cell still represents the same item.

## Gotchas
- Capturing the cell in async completion handlers shows images in wrong rows; check the index path/model identity.
- Data source and delegate are weak properties: keep strong references.

## Self-check
Scroll fast with async image loading and verify no wrong images appear.
