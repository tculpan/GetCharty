# Design Bravo: Wizard-Style Interface

## Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                    📊 GetCharty Analytics                      │
│              Transform your data into insights                 │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  [STEP 1] [STEP 2] [STEP 3] [STEP 4] [STEP 5] [PREVIEW]     │
│  Upload    Layout   Design   Chart    Advanced  Generate     │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    STEP 1: UPLOAD DATA                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │              DRAG & DROP ZONE                          │   │
│  │                                                         │   │
│  │              📁 Drop your CSV or Excel file here       │   │
│  │                                                         │   │
│  │              [Browse Files]                             │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    STEP 2: DATA LAYOUT                 │   │
│  │                                                         │   │
│  │  ┌─────────────────┐ ┌─────────────────┐               │   │
│  │  │                 │ │                 │               │   │
│  │  │   VERTICAL      │ │  HORIZONTAL     │               │   │
│  │  │   LAYOUT        │ │   LAYOUT        │               │   │
│  │  │                 │ │                 │               │   │
│  │  │  📊             │ │  📈             │               │   │
│  │  │  │              │ │  ───            │               │   │
│  │  │  │              │ │  ───            │               │   │
│  │  │  │              │ │  ───            │               │   │
│  │  │  └──────────────┘ │  ───            │               │   │
│  │  │                   │                 │               │   │
│  │  └─────────────────┘ └─────────────────┘               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    STEP 3: DESIGN ELEMENTS              │   │
│  │                                                         │   │
│  │  ┌─────────────────┐ ┌─────────────────┐               │   │
│  │  │   MACRO ITEMS   │ │   MICRO ITEMS   │               │   │
│  │  │                 │ │                 │               │   │
│  │  │ Title: [_____]  │ │ X-Axis: [_____] │               │   │
│  │  │ Subtitle: [___] │ │ Y-Axis: [_____] │               │   │
│  │  │ Footnote: [___] │ │ Y-Prefix: [___] │               │   │
│  │  │ Source: [_____] │ │ Y-Suffix: [___] │               │   │
│  │  │                 │ │                 │               │   │
│  │  └─────────────────┘ └─────────────────┘               │   │
│  │                                                         │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │              BINARY CONTROLS                    │   │   │
│  │  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │   │   │
│  │  │ │H-Ln │ │V-Ln │ │X-Lbl│ │X-Sp │ │Y-Lbl│ │Y-Sp │ │   │   │
│  │  │ │[ON] │ │[OFF]│ │[ON] │ │[ON] │ │[ON] │ │[TOP]│ │   │   │
│  │  │ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    STEP 4: CHART TYPE                  │   │
│  │                                                         │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │   │
│  │  │ 📊  │ │ 📈  │ │ 🍕  │ │ 📉  │ │ 📊  │ │ 📊  │     │   │
│  │  │ Bar  │ │Line │ │Pie  │ │Scat │ │Hist │ │Box  │     │   │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘     │   │
│  │                                                         │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                     │   │
│  │  │ 📊  │ │ 📊  │ │ 📊  │ │ 📊  │                     │   │
│  │  │Heat │ │3D   │ │Area │ │Bub  │                     │   │
│  │  └─────┘ └─────┘ └─────┘ └─────┘                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    STEP 5: ADVANCED                     │   │
│  │                                                         │   │
│  │  ┌─────────────────┐ ┌─────────────────┐               │   │
│  │  │   COLOR SCHEME  │ │   FONT STYLE    │               │   │
│  │  │                 │ │                 │               │   │
│  │  │ [Color Palette] │ │ [Font Family]   │               │   │
│  │  │                 │ │                 │               │   │
│  │  │ [Grid Colors]   │ │ [Font Size]     │               │   │
│  │  │                 │ │                 │               │   │
│  │  │ [Axis Colors]   │ │ [Font Weight]   │               │   │
│  │  │                 │ │                 │               │   │
│  │  └─────────────────┘ └─────────────────┘               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    PREVIEW & GENERATE                   │   │
│  │                                                         │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │              CHART PREVIEW                      │   │   │
│  │  │                                                 │   │   │
│  │  │                                                 │   │   │
│  │  │                                                 │   │   │
│  │  │                                                 │   │   │
│  │  │                                                 │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  [← Previous] [Generate Chart] [Export] [Save]        │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Design Philosophy
**Wizard-Style Interface**: Step-by-step process that guides users through each stage of chart creation. Each step is focused and uncluttered, with clear progression indicators. Uses visual previews and intuitive navigation.

## Key Features
- **Step-by-step workflow**: Clear progression through upload → layout → design → chart type → advanced → preview
- **Visual layout selection**: Radio buttons with preview icons for vertical/horizontal
- **Drag & drop upload**: Modern file upload interface
- **Progressive disclosure**: Advanced options in final step
- **Live preview**: Real-time chart preview in final step
- **Navigation breadcrumbs**: Clear indication of current step
- **Back/forward navigation**: Easy step navigation 