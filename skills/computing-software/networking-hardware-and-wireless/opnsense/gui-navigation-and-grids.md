---
id: computing-software.networking-hardware-and-wireless.opnsense.gui-navigation-and-grids
name: gui-navigation-and-grids
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [web-gui, navigation, favorites, data-grid, login]
level: intro
status: docs-checked
description: "Navigate the OPNsense GUI: lobby, three-level menu, favorites, type-ahead search, status colours, form help, advanced mode and data grid actions."
sources: ["https://docs.opnsense.org/manual/gui.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GUI navigation, forms and grids

Default login is user root with password opnsense (change it). The logo always returns to the Lobby, where you can see the dashboard, read the BSD license, change your password or log out.

The menu has three levels: category, function, and configuration (absent for simple functions). Favorites: hover over (or tap) the page title and click the star to toggle it; favorites appear at the top of the menu. The type-ahead search box in the upper right (click or press tab) jumps straight to a page.

The system status indicator beside your username and the firewall's domain is grey when all is well; blue is informational, yellow a warning, red an error (usually leading to the crash reporter). The firewall name is changed in System > Settings > General.

Forms: a toggle at the form's top right shows all help text at once; the (i) beside a field shows single-item help; advanced mode (bottom left of the form) reveals hidden options. Tabs can be standard or dropdown.

Data grids: the list icon selects visible columns; the search input tokenizes space-separated words and returns records that match all of them; a reload button and rows-per-page selector sit beside it. In log views each record has a "Go to page" action that jumps to surrounding context. Row actions: enable/disable, edit, copy and edit, delete (usually confirmed), and add. Page navigation buttons exist, but for large datasets such as intrusion alerts and logs the last page and total count are only estimates, since the dataset size is unknown upfront.

## Checked

2026-11-03. Confirmed against the OPNsense General User Interface manual page: login, lobby, menu levels, favorites, search, status colours, form help and advanced mode, tabs, grid features and the page navigation note. Nothing removed.

Method: documentation only; no commands were run.
