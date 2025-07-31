# Design Hotel: Minimalist Sidebar Layout

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
│   MINIMAL SIDE  │ │              MAIN CONTENT                  │
│                 │ │                                             │
│ 📁 FILE UPLOAD  │ │ ┌─────────────────────────────────────────┐ │
│ ┌─────────────┐ │ │ │           CHART TYPE SELECTOR          │ │
│ │ Choose File │ │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │ │
│ └─────────────┘ │ │ │ │ 📊  │ │ 📈  │ │ 🍕  │ │ 📉  │       │ │
│                 │ │ │ │ Bar  │ │Line │ │Pie  │ │Scat │       │ │
│ 📐 ORIENTATION │ │ │ │ └─────┘ └─────┘ └─────┘ └─────┘       │ │
│ ┌─────────────┐ │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │ │
│ │ ○ --        │ │ │ │ │ 📊  │ │ 📈  │ │ 📊  │ │ 📊  │       │ │
│ │ ● |         │ │ │ │ │Hist │ │Box  │ │Heat │ │3D   │       │ │
│ └─────────────┘ │ │ │ │ └─────┘ └─────┘ └─────┘ └─────┘       │ │
│                 │ │ └─────────────────────────────────────────┘ │
│ 🎯 GENERATE    │ │                                             │
│ [Generate Chart]│ │ ┌─────────────────────────────────────────┐ │
│                 │ │ │           CHART TITLES                 │ │
│                 │ │ │ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │
│                 │ │ │ │ Title   │ │Subtitle │ │Footnote │   │ │
│                 │ │ │ └─────────┘ └─────────┘ └─────────┘   │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │
│                 │ │ │ │ Source                              │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │
│                 │ │ └─────────────────────────────────────────┘ │
│                 │ │ ┌─────────────────────────────────────────┐ │
│                 │ │ │           AXES LABELS                 │ │
│                 │ │ │ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │
│                 │ │ │ │X-Axis   │ │Y-Axis   │ │Y-Prefix │   │ │
│                 │ │ │ └─────────┘ └─────────┘ └─────────┘   │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │
│                 │ │ │ │ Y-Suffix                            │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │
│                 │ │ └─────────────────────────────────────────┘ │
│                 │ │ ┌─────────────────────────────────────────┐ │
│                 │ │ │           BINARY CONTROLS              │ │
│                 │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │ │
│                 │ │ │ │H-Ln │ │V-Ln │ │X-Lbl│ │X-Sp │       │ │
│                 │ │ │ │[ON] │ │[OFF]│ │[ON] │ │[ON] │       │ │
│                 │ │ │ └─────┘ └─────┘ └─────┘ └─────┘       │ │
│                 │ │ │ ┌─────┐ ┌─────┐                       │ │
│                 │ │ │ │Y-Lbl│ │Y-Sp │                       │ │
│                 │ │ │ │[ON] │ │[TOP]│                       │ │
│                 │ │ │ └─────┘ └─────┘                       │ │
│                 │ │ └─────────────────────────────────────────┘ │
│                 │ │ ┌─────────────────────────────────────────┐ │
│                 │ │ │           ADVANCED OPTIONS             │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │
│                 │ │ │ │ ▼ More Options                      │ │ │
│                 │ │ │ │ • Color Schemes                     │ │ │
│                 │ │ │ │ • Font Selection                    │ │ │
│                 │ │ │ │ • Grid Styling                      │ │ │
│                 │ │ │ │ • Animation Settings                │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │
│                 │ │ └─────────────────────────────────────────┘ │
└─────────────────┘ └─────────────────────────────────────────────┘
```

## Design Philosophy
**Minimalist Sidebar Layout**: Clean, minimal sidebar with essential controls, while the main content area focuses on chart type selection and design elements. The chart type selector is prominently positioned at the top of the main content area.

## Key Features
- **Dark theme**: Based on Design-Echo's purple-pink gradient
- **Minimal sidebar**: Only essential controls (file upload, orientation, generate)
- **Prominent chart selector**: Positioned at the top of main content
- **Visual orientation icons**: Horizontal (--) and vertical (|) lines
- **Renamed sections**: "Chart Titles" and "Axes Labels"
- **No separate upload button**: Executes on Generate Chart only
- **Compact layout**: Smaller, more focused elements
- **No green colors**: Avoiding disliked green from Design-Charlie 