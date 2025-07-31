# Design Alpha: Clean Dashboard Layout

## Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                    📊 GetCharty Analytics                      │
│              Transform your data into insights                 │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────┐ ┌─────────────────────────────────────────────┐
│   SIDEBAR       │ │              MAIN CONTENT                  │
│                 │ │                                             │
│ 📁 File Upload  │ │ ┌─────────────────────────────────────────┐ │
│ ┌─────────────┐ │ │ │                                         │ │
│ │ Choose File │ │ │ │           CHART DISPLAY                 │ │
│ │ [Browse...] │ │ │ │                                         │ │
│ │ [Upload]    │ │ │ │                                         │ │
│ └─────────────┘ │ │ │                                         │ │
│                 │ │ └─────────────────────────────────────────┘ │
│ 📐 Data Layout │ │                                             │
│ ┌─────────────┐ │ │ ┌─────────────────────────────────────────┐ │
│ │ ○ Vertical  │ │ │ │           DESIGN PANEL                  │ │
│ │ ● Horizontal│ │ │ │ ┌─────────────────────────────────────┐ │ │
│ └─────────────┘ │ │ │ │           MACRO ELEMENTS            │ │ │
│                 │ │ │ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │ │
│ 🎯 Generate    │ │ │ │ │ Title   │ │Subtitle │ │Footnote │ │ │ │
│ [Create Chart] │ │ │ │ └─────────┘ └─────────┘ └─────────┘ │ │ │
│                 │ │ │ │ ┌─────────────────────────────────┐ │ │ │
│                 │ │ │ │ │ Source                          │ │ │ │
│                 │ │ │ │ └─────────────────────────────────┘ │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │
│                 │ │ │ │           MICRO ELEMENTS            │ │ │
│                 │ │ │ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ │ │ │
│                 │ │ │ │ │X-Axis   │ │Y-Axis   │ │Y-Prefix │ │ │ │
│                 │ │ │ │ └─────────┘ └─────────┘ └─────────┘ │ │ │
│                 │ │ │ │ ┌─────────────────────────────────┐ │ │ │
│                 │ │ │ │ │ Y-Suffix                        │ │ │ │
│                 │ │ │ │ └─────────────────────────────────┘ │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │
│                 │ │ │ │         BINARY CONTROLS             │ │ │
│                 │ │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │ │ │
│                 │ │ │ │ │H-Ln │ │V-Ln │ │X-Lbl│ │X-Sp │   │ │ │
│                 │ │ │ │ │[ON] │ │[OFF]│ │[ON] │ │[ON] │   │ │ │
│                 │ │ │ │ └─────┘ └─────┘ └─────┘ └─────┘   │ │ │
│                 │ │ │ │ ┌─────┐ ┌─────┐                   │ │ │
│                 │ │ │ │ │Y-Lbl│ │Y-Sp │                   │ │ │
│                 │ │ │ │ │[ON] │ │[TOP]│                   │ │ │
│                 │ │ │ │ └─────┘ └─────┘                   │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │
│                 │ │ │ │         CHART TYPE SELECTOR         │ │ │
│                 │ │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │ │ │
│                 │ │ │ │ │ 📊  │ │ 📈  │ │ 🍕  │ │ 📉  │   │ │ │
│                 │ │ │ │ │ Bar  │ │Line │ │Pie  │ │Scat │   │ │ │
│                 │ │ │ │ └─────┘ └─────┘ └─────┘ └─────┘   │ │ │
│                 │ │ │ │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │ │ │
│                 │ │ │ │ │ 📊  │ │ 📈  │ │ 📊  │ │ 📊  │   │ │ │
│                 │ │ │ │ │Hist │ │Box  │ │Heat │ │3D   │   │ │ │
│                 │ │ │ │ └─────┘ └─────┘ └─────┘ └─────┘   │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │
│                 │ │ │ ┌─────────────────────────────────────┐ │ │
│                 │ │ │ │         ADVANCED OPTIONS            │ │ │
│                 │ │ │ │ ┌─────────────────────────────────┐ │ │ │
│                 │ │ │ │ │ ▼ More Options                  │ │ │ │
│                 │ │ │ │ │ • Color Schemes                 │ │ │ │
│                 │ │ │ │ │ • Font Selection                │ │ │ │
│                 │ │ │ │ │ • Grid Styling                  │ │ │ │
│                 │ │ │ │ │ • Animation Settings            │ │ │ │
│                 │ │ │ │ └─────────────────────────────────┘ │ │ │
│                 │ │ │ └─────────────────────────────────────┘ │ │
│                 │ │ └─────────────────────────────────────────┘ │
└─────────────────┘ └─────────────────────────────────────────────┘
```

## Design Philosophy
**Minimalist Dashboard**: Clean, card-based layout with clear visual hierarchy. Sidebar contains core functions, main area focuses on chart display and design controls. Uses subtle shadows and rounded corners for modern feel.

## Key Features
- **Card-based organization**: Each functional area is contained in its own card
- **Progressive disclosure**: Advanced options hidden in dropdown
- **Icon-based chart selection**: Visual chart type picker
- **Toggle switches**: Modern binary controls
- **Three-way toggle**: For Y-axis spacing (Off/On/Top Only)
- **Responsive layout**: Sidebar collapses on smaller screens 