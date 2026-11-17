---
id: computing-software.game-programming.unity.lateupdate-camera-follow
name: lateupdate-camera-follow
category: computing-software
field: game-programming
product: unity
tags: [unity, monobehaviour, lateupdate-camera-follow, camera-follow, execution-order, game-programming]
level: practitioner
status: docs-checked
description: "Use LateUpdate for a Unity follow camera so it tracks objects moved in Update, and know where physics simulation lands relative to FixedUpdate and Update."
sources: ["https://docs.unity3d.com/Manual/execution-order.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.LateUpdate.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LateUpdate for camera follow

**Goal:** a follow camera that reads target positions after they have moved this frame. Unity 6000.x docs.

## What the docs say
- `LateUpdate()` is called every frame if the Behaviour is enabled, after all `Update` functions have been called.
- The script reference's own guidance: a follow camera should always be implemented in `LateUpdate` because it tracks
  objects that might have moved inside `Update`.

```csharp
public class FollowCam : MonoBehaviour
{
    [SerializeField] Transform target;
    [SerializeField] Vector3 offset = new Vector3(0, 3, -6);

    void LateUpdate()
    {
        transform.position = target.position + offset;
        transform.LookAt(target);
    }
}
```
(Illustrative only: the pages do not show a camera sample; the script reference's example is a `LateUpdate` that calls
`transform.Translate`.)

## Where physics runs relative to Update
The physics simulation step includes collision detection, Rigidbody and joint integration, writing body poses back to
Transforms, and the physics callbacks (`OnTriggerEnter`, `OnCollisionEnter`, `OnJointBreak`, `OnParticleCollision` and
others). When it runs depends on `Physics.simulationMode` / `Physics2D.simulationMode`:
- `FixedUpdate` mode: directly after `MonoBehaviour.FixedUpdate`.
- `Update` mode: directly after `MonoBehaviour.Update`.
- `Script` mode: when you call `Physics.Simulate` / `Physics2D.Simulate`.

So with `FixedUpdate` mode, body poses change only on physics steps, not every rendered frame.

## Ordering limits
You cannot rely on the order in which the same event function runs on different GameObjects, or on different instances of
the same script, unless the order is documented or settable. Use Script execution order to order different MonoBehaviour
scripts.

## Checked
Date: 2026-11-07.
Read in full: "Event function execution order" manual page (6000.6 docs) and the `MonoBehaviour.LateUpdate` script
reference. The page's execution-order diagram is an image, so the exact position of the Animator update relative to
`LateUpdate` is not confirmed by the text.
Removed as unconfirmed: the full frame sequence with Animator update before `LateUpdate`, `[DefaultExecutionOrder(100)]`,
`SmoothDamp` and `Lerp` smoothing advice, the Rigidbody interpolation jitter fixes, the Animator "Animate Physics" and bone
override remarks, Cinemachine Brain update methods, the UI `WorldToScreenPoint` ordering note and the invented Verify
checklist.
Method: documentation only; no commands were run.
