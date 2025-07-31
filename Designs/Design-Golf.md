# Design Golf: Floating Panel Layout

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
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │   FILE UPLOAD   │ │ DATA ORIENTATION│ │ CHART TYPE      │   │
│  │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────────┐ │   │
│  │ │ Choose File │ │ │ │ ○ --        │ │ │ │ 📊 Bar      │ │   │
│  │ └─────────────┘ │ │ │ ● |         │ │ │ │ 📈 Line     │ │   │
│  │                 │ │ │ └─────────────┘ │ │ │ 🍕 Pie      │ │   │
│  │ [Generate Chart]│ │ │                 │ │ │ 📉 Scat     │ │   │
│  │                 │ │ │                 │ │ │ 📊 Hist     │ │   │
│  └─────────────────┘ │ │                 │ │ │ 📈 Box      │ │   │
│                      │ │                 │ │ │ 📊 Heat     │ │   │
│                      │ │                 │ │ │ 📊 3D       │ │   │
│                      │ └─────────────────┘ │ └─────────────┘ │   │
│                      └─────────────────────┴─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              CHART TITLES & AXES LABELS                │   │
│  │ ┌─────────────────┐ ┌─────────────────┐               │   │
│  │ │   CHART TITLES  │ │   AXES LABELS   │               │   │
│  │ │ ┌─────────────┐ │ │ ┌─────────────┐ │               │   │
│  │ │ │ Title       │ │ │ │ X-Axis      │ │               │   │
│  │ │ │ Subtitle    │ │ │ │ Y-Axis      │ │               │   │
│  │ │ │ Footnote    │ │ │ │ Y-Prefix    │ │               │   │
│  │ │ │ Source      │ │ │ │ Y-Suffix    │ │               │   │
│  │ │ └─────────────┘ │ │ └─────────────┘ │               │   │
│  │ └─────────────────┘ └─────────────────┘               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              BINARY CONTROLS & ADVANCED                │   │
│  │ ┌─────────────────┐ ┌─────────────────┐               │   │
│  │ │ BINARY CONTROLS │ │ ADVANCED OPTIONS│               │   │
│  │ │ ┌─────┐ ┌─────┐ │ │ ┌─────────────┐ │               │   │
│  │ │ │H-Ln │ │V-Ln │ │ │ │ ▼ More      │ │               │   │
│  │ │ │X-Lbl│ │X-Sp │ │ │ │ Options      │ │               │   │
│  │ │ │Y-Lbl│ │Y-Sp │ │ │ └─────────────┘ │               │   │
│  │ │ └─────┘ └─────┘ │ │                 │               │   │
│  │ └─────────────────┘ └─────────────────┘               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Design Philosophy
**Floating Panel Layout**: Compact, floating panels with the chart type selector positioned prominently near the chart display. Simplified file upload and data orientation, with a clean separation of concerns.

## Key Features
- **Dark theme**: Based on Design-Echo's purple-pink gradient
- **Floating panels**: Compact, focused sections
- **Prominent chart selector**: Positioned near the chart display
- **Visual orientation icons**: Horizontal (--) and vertical (|) lines
- **Renamed sections**: "Chart Titles" and "Axes Labels"
- **No separate upload button**: Executes on Generate Chart only
- **Compact layout**: Smaller, more focused elements
- **No green colors**: Avoiding disliked green from Design-Charlie 