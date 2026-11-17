---
id: computing-software.computer-graphics-engineering.opencv.opencv-highgui-backends-and-headless-servers
name: opencv-highgui-backends-and-headless-servers
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, highgui, highgui-qt, headless-display, qt-platform-plugin]
level: practitioner
status: docs-checked
description: "Fix OpenCV HighGUI issues: GTK vs Qt vs Win32 backends, 'function not implemented' in headless wheels, Qt plugin conflicts with PyQt, and displaying on servers/notebooks."
sources: ["https://docs.opencv.org/4.x/d7/dfc/group__highgui.html", "https://github.com/opencv/opencv-python/blob/main/README.md", "https://github.com/opencv/opencv/blob/4.x/doc/tutorials/introduction/env_reference/env_reference.markdown", "https://github.com/opencv/opencv/blob/4.x/doc/tutorials/introduction/config_reference/config_reference.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HighGUI backends and headless environments

## Which backend you have
`print(cv2.getBuildInformation())` shows the GUI section of your build. The opencv-python README states that non-headless Linux wheels ship
with Qt 5 and that the headless packages have no GUI library dependencies. Without a GUI backend, `cv2.imshow` raises
`The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support.` (the message text in `window.cpp`; the status code is `StsNotImplemented`).

## Common failures and fixes
| Error | Cause | Fix |
|---|---|---|
| "function is not implemented" in imshow | headless wheel or built without GUI | install a non-headless package where you need windows, or don't call imshow |
| Qt platform plugin load error | Qt plugin or display library problem (the OpenCV docs do not cover this) | diagnose with the Qt documentation; if you need no OpenCV windows, use a headless package |
| no display on SSH | no X server | write images to disk or use another display route |
| window opens then freezes | `waitKey` or `pollKey` not called, so GUI events are not processed | call `cv2.waitKey(1)` in the loop |
| Two OpenCV installs conflict | several packages installed in one environment | the opencv-python README says to select only one of the four packages (all use the `cv2` namespace; there is no plugin architecture) and to remove manually installed copies |

## Displaying without HighGUI
- **Jupyter:** `from IPython.display import display, Image; display(Image(data=cv2.imencode('.png', img)[1].tobytes()))`
  or `plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))`.
- **Servers / web:** encode JPEG frames (`cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])`) and send them
  with your web stack.
- **Docker:** prefer the headless package in images that never show windows.

## Picking a backend explicitly
Building from source, the config reference lists `WITH_GTK` (default ON, Linux; GTK 3 if found, `WITH_GTK_2_X` forces 2),
`WITH_WIN32UI` (default ON, Windows) and `WITH_QT` (default OFF). A Qt build enables the advanced highgui interface (`displayOverlay`,
`createButton`, `WINDOW_GUI_EXPANDED`; see the highgui Qt group). At runtime `OPENCV_UI_BACKEND` chooses one of `GTK`, `GTK3`, `GTK2`, `QT`, `WIN32`, and
`OPENCV_UI_PRIORITY_LIST` orders backends. `namedWindow(name, cv2.WINDOW_NORMAL)` makes the window resizable.

## Verify
- [ ] Build info shows the intended GUI backend (or NONE on servers); no Qt plugin warnings at startup.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/highgui/include/opencv2/highgui.hpp, modules/highgui/src/window.cpp, doc/tutorials/introduction/config_reference and env_reference, and the opencv-python README. Confirmed: not-implemented message, WITH_GTK / WITH_WIN32UI / WITH_QT defaults, OPENCV_UI_BACKEND values, Qt-only functions, waitKey/pollKey event handling, README statements on Qt in Linux wheels and on installing one package only. Removed the unconfirmed apt packages, QT_QPA variable, xvfb, ssh -X and X11 socket advice.
Method: documentation only; no commands were run.
