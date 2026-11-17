---
id: computing-software.computer-graphics-engineering.opencv.opencv-highgui-imshow-trackbars-and-mouse
name: opencv-highgui-imshow-trackbars-and-mouse
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, highgui, imshow, waitkey, trackbar, setmousecallback, selectroi, namedwindow, opencv-python-headless, parameter-tuning]
level: practitioner
status: docs-checked
description: "Build quick OpenCV tuning tools with highgui: imshow/waitKey event loop, trackbars for thresholds, mouse callbacks and selectROI, plus the headless and threading pitfalls."
sources: ["https://docs.opencv.org/4.x/d7/dfc/group__highgui.html", "https://github.com/opencv/opencv/blob/4.x/modules/highgui/include/opencv2/highgui.hpp", "https://github.com/opencv/opencv-python/blob/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV HighGUI: imshow, trackbars and mouse

**Goal:** interactive parameter tuning and annotation tools in minutes, without the
frozen-window and headless-crash surprises.

## 1. The event loop
```python
cv2.namedWindow("view", cv2.WINDOW_NORMAL)        # resizable; WINDOW_AUTOSIZE (default) = size fits the image
while True:
    cv2.imshow("view", frame)
    k = cv2.waitKey(1) & 0xFF                      # processes GUI events; delay 0 (or negative) = wait forever
    if k in (27, ord('q')): break
    if cv2.getWindowProperty("view", cv2.WND_PROP_VISIBLE) < 1: break   # user closed window
cv2.destroyAllWindows()
```
Per the docs, `waitKey` and `pollKey` are the only HighGUI functions that fetch and handle GUI events, so call one of them
periodically; a frozen window usually means neither runs. `waitKey(delay)` waits at least `delay` ms, depending on what else is running, and
returns -1 if no key was pressed. `waitKeyEx` returns the full key code (use it for keys such as arrows; codes are platform-specific).

## 2. Trackbars for live tuning
```python
def nothing(_): pass
cv2.createTrackbar("lowH", "view", 0, 179, nothing)
cv2.createTrackbar("highH", "view", 179, 179, nothing)
while True:
    lo = cv2.getTrackbarPos("lowH", "view"); hi = cv2.getTrackbarPos("highH", "view")
    mask = cv2.inRange(hsv, (lo, 50, 50), (hi, 255, 255))
    cv2.imshow("view", mask)
    if cv2.waitKey(30) == 27: break
print("final", lo, hi)                            # paste into config
```
Trackbar values are integers up to the maximum you pass: map to floats yourself (`val / 100.0`), and enforce odd kernel
sizes with `k = 2*v + 1`.

## 3. Mouse callbacks and ROI selection
```python
pts = []
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: pts.append((x, y))
cv2.setMouseCallback("view", on_mouse)
x, y, w, h = cv2.selectROI("view", frame, showCrosshair=True)   # space or enter finishes, c cancels
```
`selectROI` returns an empty rect when the selection is cancelled and installs its own mouse callback on the window, then sets an empty callback
afterwards, so call `setMouseCallback` again after it. For a resized `WINDOW_NORMAL` window, check whether your backend reports
callback coordinates in image or window pixels.

## 4. Headless environments
Builds without a GUI backend (such as the headless packages) raise `The function is not implemented` from `imshow`. In servers,
notebooks and Docker use `cv2.imwrite` or matplotlib (`plt.imshow(img[..., ::-1])`). The opencv-python README says to install only one of
its four packages per environment.

## Gotchas
- `imshow` scaling per the docs: 16-bit unsigned pixels are divided by 256, and 32-bit or 64-bit floating-point pixels are multiplied by 255, so float images should be in [0,1].
- With the Qt backend, `WINDOW_GUI_EXPANDED` gives a status bar and tool bar; other backends do not.
- Only windows created without `WINDOW_AUTOSIZE` can be resized.

## Verify
- [ ] Closing the window with the X button exits the loop (no zombie loop).
- [ ] Tool prints the final tuned parameters for copy into config.
- [ ] Server code paths don't import or call highgui.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/highgui/include/opencv2/highgui.hpp, modules/highgui/src/window.cpp, doc/tutorials/introduction/config_reference and env_reference, and the opencv-python README. Confirmed: WINDOW_NORMAL and WINDOW_AUTOSIZE semantics, WND_PROP_VISIBLE, waitKey and pollKey behaviour, selectROI controls and callback handling, imshow float and 16-bit scaling. Removed the unconfirmed latency figure, macOS main-thread statement and Qt/Win32 layout statement.
Method: documentation only; no commands were run.
