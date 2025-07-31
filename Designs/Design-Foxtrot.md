# Design Foxtrot: Compact Dark Theme

## Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│  🌙 GetCharty Analytics  [☰] [💾] [📤] [⚙️] [🌙]             │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    CHART DISPLAY                        │   │
│  │                                                         │   │
│  │                                                         │   │
│  │                                                         │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────┐ ┌─────────────────────────────────────────────┐
│   COMPACT PANEL │ │              DESIGN WORKSPACE              │
│                 │ │                                             │
│ 📁 FILE UPLOAD  │ │ ┌─────────────────────────────────────────┐ │
│ ┌─────────────┐ │ │ │           CHART TITLES                 │ │
│ │ Choose File │ │ │ │ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │
│ └─────────────┘ │ │ │ │ Title   │ │Subtitle │ │Footnote │   │ │
│                 │ │ │ └─────────┘ └─────────┘ └─────────┘   │ │
│ 📐 ORIENTATION │ │ │ ┌─────────────────────────────────────┐ │ │
│ ┌─────────────┐ │ │ │ │ Source                              │ │ │
│ │ ○ --        │ │ │ │ └─────────────────────────────────────┘ │ │
│ │ ● |         │ │ │ └─────────────────────────────────────────┘ │ │
│ └─────────────┘ │ │ ┌─────────────────────────────────────────┐ │ │
│                 │ │ │           AXES LABELS                  │ │ │
│ 🎯 GENERATE    │ │ │ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │ │
│ [Generate Chart]│ │ │ │X-Axis   │ │Y-Axis   │ │Y-Prefix │   │ │ │
│                 │ │ │ └─────────┘ └─────────┘ └─────────┘   │ │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │ │
│                 │ │ │ │ Y-Suffix                            │ │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │ │
│                 │ │ └─────────────────────────────────────────┘ │ │
│                 │ │ ┌─────────────────────────────────────────┐ │ │
│                 │ │ │           BINARY CONTROLS              │ │ │
│                 │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │ │ │
│                 │ │ │ │H-Ln │ │V-Ln │ │X-Lbl│ │X-Sp │       │ │ │
│                 │ │ │ │[ON] │ │[OFF]│ │[ON] │ │[ON] │       │ │ │
│                 │ │ │ └─────┘ └─────┘ └─────┘ └─────┘       │ │ │
│                 │ │ │ ┌─────┐ ┌─────┐                       │ │ │
│                 │ │ │ │Y-Lbl│ │Y-Sp │                       │ │ │
│                 │ │ │ │[ON] │ │[TOP]│                       │ │ │
│                 │ │ │ └─────┘ └─────┘                       │ │ │
│                 │ │ └─────────────────────────────────────────┘ │ │
│                 │ │ ┌─────────────────────────────────────────┐ │ │
│                 │ │ │           CHART TYPE SELECTOR          │ │ │
│                 │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │ │ │
│                 │ │ │ │ 📊  │ │ 📈  │ │ 🍕  │ │ 📉  │       │ │ │
│                 │ │ │ │ Bar  │ │Line │ │Pie  │ │Scat │       │ │ │
│                 │ │ │ └─────┘ └─────┘ └─────┘ └─────┘       │ │ │
│                 │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │ │ │
│                 │ │ │ │ 📊  │ │ 📈  │ │ 📊  │ │ 📊  │       │ │ │
│                 │ │ │ │Hist │ │Box  │ │Heat │ │3D   │       │ │ │
│                 │ │ │ └─────┘ └─────┘ └─────┘ └─────┘       │ │ │
│                 │ │ └─────────────────────────────────────────┘ │ │
│                 │ │ ┌─────────────────────────────────────────┐ │ │
│                 │ │ │           ADVANCED OPTIONS              │ │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │ │
│                 │ │ │ │ ▼ More Options                      │ │ │ │
│                 │ │ │ │ • Color Schemes                     │ │ │ │
│                 │ │ │ │ • Font Selection                    │ │ │ │
│                 │ │ │ │ • Grid Styling                      │ │ │ │
│                 │ │ │ │ • Animation Settings                │ │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │ │
│                 │ │ └─────────────────────────────────────────┘ │ │
└─────────────────┘ └─────────────────────────────────────────────┘
```

## Design Philosophy
**Compact Dark Theme**: Streamlined layout with dark aesthetics from Design-Echo, simplified file upload (no separate upload button), compact data orientation with visual icons, and chart type selector positioned near the chart display area.

## Key Features
- **Dark theme**: Based on Design-Echo's purple-pink gradient
- **Compact file upload**: No separate upload button, executes on Generate Chart
- **Visual orientation icons**: Horizontal line (--) and vertical line (|) for data orientation
- **Renamed sections**: "Chart Titles" and "Axes Labels" instead of Macro/Micro
- **Positioned chart selector**: Near the chart display area
- **Simplified layout**: Smaller, more focused elements
- **No green colors**: Avoiding the disliked green from Design-Charlie 