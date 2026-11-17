---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-controltemplate-visualstates
name: wpf-controltemplate-visualstates
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-controltemplate-visualstates, wpf-templates-styles, wpf, controltemplate, datatemplate, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Restyle a control with ControlTemplate, TemplateBinding, ContentPresenter and VisualStateManager."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/styles-templates-overview
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/templatebinding-markup-extension
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF ControlTemplate and VisualStateManager

**Goal:** custom look without losing behaviour.

```xml
<Style TargetType="Button">
  <Setter Property="Template">
    <Setter.Value>
      <ControlTemplate TargetType="Button">
        <Border x:Name="bd" Background="{TemplateBinding Background}" Padding="{TemplateBinding Padding}">
          <VisualStateManager.VisualStateGroups>
            <VisualStateGroup x:Name="CommonStates">
              <VisualState x:Name="Normal"/>
              <VisualState x:Name="MouseOver"/>   <!-- add Storyboards to animate -->
            </VisualStateGroup>
          </VisualStateManager.VisualStateGroups>
          <ContentPresenter HorizontalAlignment="Center"/>
        </Border>
      </ControlTemplate>
    </Setter.Value>
  </Setter>
</Style>
```

**Gotcha:** You cannot patch part of a control's visual tree: set a whole new `ControlTemplate`, then re-supply the states (such as Focused/Unfocused and the CommonStates) you still want. `TemplateBinding` is the optimised binding form for templates, and a `ContentPresenter` in a ContentControl template binds to the control's content automatically.

## Verify
- Hover, pressed, disabled and keyboard focus are all visibly different once you add the state animations.

## Checked

2026-11-03. Confirmed in the WPF styles and templates overview: replacing the entire ControlTemplate, `TemplateBinding`, `ContentPresenter` auto-binding, `VisualStateManager` on the template root with the `CommonStates` (Normal, MouseOver) and `FocusStates` groups. Removed: PART_ naming advice, and IsMouseOver/IsEnabled triggers and CornerRadius, which that page does not cover.

Method: documentation only; no commands were run.
