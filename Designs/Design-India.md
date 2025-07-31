# Design India: Tabbed Interface Layout

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
│  [📁 UPLOAD] [📐 ORIENTATION] [📊 CHART TYPE] [📝 TITLES] [⚙️ CONTROLS] │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    TAB CONTENT                          │   │
│  │                                                         │   │
│  │  ┌─────────────────┐ ┌─────────────────┐               │   │
│  │  │   FILE UPLOAD   │ │ DATA ORIENTATION│               │   │
│  │  │ ┌─────────────┐ │ │ ┌─────────────┐ │               │   │
│  │  │ │ Choose File │ │ │ │ ○ --        │ │               │   │
│  │  │ └─────────────┘ │ │ │ ● |         │ │               │   │
│  │  │                 │ │ │ └─────────────┘ │               │   │
│  │  │ [Generate Chart]│ │ │                 │               │   │
│  │  └─────────────────┘ │ │                 │               │   │
│  │                      │ └─────────────────┘               │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │              CHART TYPE SELECTOR               │   │   │
│  │  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │   │   │
│  │  │ │ 📊  │ │ 📈  │ │ 🍕  │ │ 📉  │ │ 📊  │ │ 📈  │ │   │   │
│  │  │ │ Bar  │ │Line │ │Pie  │ │Scat │ │Hist │ │Box  │ │   │   │
│  │  │ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ │   │   │
│  │  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐               │   │   │
│  │  │ │ 📊  │ │ 📊  │ │ 📊  │ │ 📊  │               │   │   │
│  │  │ │Heat │ │3D   │ │Area │ │Bub  │               │   │   │
│  │  │ └─────┘ └─────┘ └─────┘ └─────┘               │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  ┌─────────────────┐ ┌─────────────────┐               │   │
│  │  │   CHART TITLES  │ │   AXES LABELS   │               │   │
│  │  │ ┌─────────────┐ │ │ ┌─────────────┐ │               │   │
│  │  │ │ Title       │ │ │ │ X-Axis      │ │               │   │
│  │  │ │ Subtitle    │ │ │ │ Y-Axis      │ │               │   │
│  │  │ │ Footnote    │ │ │ │ Y-Prefix    │ │               │   │
│  │  │ │ Source      │ │ │ │ Y-Suffix    │ │               │   │
│  │  │ └─────────────┘ │ │ └─────────────┘ │               │   │
│  │  └─────────────────┘ └─────────────────┘               │   │
│  │                                                         │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │              BINARY CONTROLS                   │   │   │
│  │  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │   │   │
│  │  │ │H-Ln │ │V-Ln │ │X-Lbl│ │X-Sp │ │Y-Lbl│ │Y-Sp │ │   │   │
│  │  │ │[ON] │ │[OFF]│ │[ON] │ │[ON] │ │[ON] │ │[TOP]│ │   │   │
│  │  │ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │              ADVANCED OPTIONS                  │   │   │
│  │  │ ┌─────────────────────────────────────────┐   │   │   │
│  │  │ │ ▼ More Options                          │   │   │   │
│  │  │ │ • Color Schemes                         │   │   │   │
│  │  │ │ • Font Selection                        │   │   │   │
│  │  │ │ • Grid Styling                          │   │   │   │
│  │  │ │ • Animation Settings                    │   │   │   │
│  │  │ └─────────────────────────────────────────┘   │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Design Philosophy
**Tabbed Interface Layout**: Clean tabbed navigation with the chart type selector integrated into the main workflow. Each tab focuses on a specific aspect of chart creation, with the chart type selector prominently displayed in its own tab.

## Key Features
- **Dark theme**: Based on Design-Echo's purple-pink gradient
- **Tabbed navigation**: Clean separation of concerns
- **Integrated chart selector**: Dedicated tab for chart type selection
- **Visual orientation icons**: Horizontal (--) and vertical (|) lines
- **Renamed sections**: "Chart Titles" and "Axes Labels"
- **No separate upload button**: Executes on Generate Chart only
- **Compact layout**: Smaller, more focused elements
- **No green colors**: Avoiding disliked green from Design-Charlie 