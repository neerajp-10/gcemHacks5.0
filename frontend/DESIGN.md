---
name: Earthworm Field Advisory
colors:
  surface: '#ecfef0'
  surface-dim: '#cdded1'
  surface-bright: '#ecfef0'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#e6f8ea'
  surface-container: '#e1f2e5'
  surface-container-high: '#dbeddf'
  surface-container-highest: '#d5e7da'
  on-surface: '#101f16'
  on-surface-variant: '#404942'
  inverse-surface: '#25342b'
  inverse-on-surface: '#e3f5e8'
  outline: '#707a71'
  outline-variant: '#bfc9bf'
  surface-tint: '#216b45'
  primary: '#005230'
  on-primary: '#ffffff'
  primary-container: '#216b45'
  on-primary-container: '#9fe9b9'
  inverse-primary: '#8dd6a8'
  secondary: '#57615b'
  on-secondary: '#ffffff'
  secondary-container: '#dbe5dd'
  on-secondary-container: '#5d6761'
  tertiary: '#633f00'
  on-tertiary: '#ffffff'
  tertiary-container: '#835400'
  on-tertiary-container: '#ffd095'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#a8f3c2'
  primary-fixed-dim: '#8dd6a8'
  on-primary-fixed: '#002110'
  on-primary-fixed-variant: '#005230'
  secondary-fixed: '#dbe5dd'
  secondary-fixed-dim: '#bfc9c1'
  on-secondary-fixed: '#151d19'
  on-secondary-fixed-variant: '#404943'
  tertiary-fixed: '#ffddb5'
  tertiary-fixed-dim: '#ffb957'
  on-tertiary-fixed: '#2a1800'
  on-tertiary-fixed-variant: '#643f00'
  background: '#ecfef0'
  on-background: '#101f16'
  surface-variant: '#d5e7da'
typography:
  headline-xl:
    fontFamily: Noto Sans
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 46px
  headline-xl-mobile:
    fontFamily: Noto Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 40px
  headline-lg:
    fontFamily: Noto Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 38px
  headline-md:
    fontFamily: Noto Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Noto Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Noto Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 30px
  body-md:
    fontFamily: Noto Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  label-lg:
    fontFamily: Noto Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  label-md:
    fontFamily: Noto Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 22px
  label-sm:
    fontFamily: Noto Sans
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 1.25rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system delivers a calm, dignified, and highly legible mobile-first experience tailored for smallholder paddy farmers in Mandya, Karnataka. It draws directly from the ethos of trusted public agricultural extensions—balancing functional clarity with quiet optimism.

The visual direction rejects cluttered tech interfaces, dark patterns, decorative gradients, and micro-analytics. Instead, it relies on structured utility, generous white space, and robust physical touch targets engineered for direct sunlight and one-handed operation in the field. 

The aesthetic is built around:
- **Respectful Utility**: Big, uncompressed Kannada and English text with ample vertical breath for diacritics and complex conjuncts.
- **Atmospheric Calm**: Organic agricultural greens paired with rich, unbleached earthen whites rather than stark clinical grays.
- **Field Contrast**: Distinct boundaries, 1.5px to 2px crisp borders, and zero dependence on low-contrast drop shadows, guaranteeing visibility on budget mobile screens in glaring midday light.

## Colors

The palette is tuned specifically for high ambient lux environments, utilizing organic, high-legibility hues that honor the agrarian landscape of Mandya.

- **Primary (`#216B45`)**: Deep Agricultural Green. Used for top-level navigation headers, primary action buttons, key metrics, and verified operational states.
- **Secondary / Container (`#EAF4EC`)**: Light Sage Surface. Used as the grounding tone for advisory cards, advisory banners, and grouping containers.
- **Tertiary / Accent (`#E8A23A`)**: Caution Amber. Strictly reserved for pest alerts, water-stress warnings, time-critical weather updates, and immediate advisory items.
- **Canvas / Ground (`#FAFAF6`)**: Warm Off-White. Mimics raw pulp paper, minimizing harsh glare under the sun while keeping contrast high.
- **Text & Stroke Neutral (`#26352C`)**: Charcoal Flora. High-contrast ink tone for all primary headings, body text, and line icons, providing crisp contrast without the harshness of pure `#000000`.
- **Secondary Text (`#4F6355`)**: Muted Moss. Used for metadata, subtitles, timestamps, and advisory sources.
- **Structural Border (`#D2E2D6`)**: Crisp Willow Border. Used to cleanly delineate cards and interactive zones without visual noise.
- **Informational Blue (`#2B6CB0`) & Surface (`#EBF3FA`)**: Reserved for irrigation schedules, canal water releases, and governmental mandi updates.

## Typography

The type system prioritizes multi-script harmony between Kannada (ಕನ್ನಡ) script and Latin characters. Kannada script relies heavily on complex ottakshara (subscript conjunct consonants) and vowel matras above and below the base characters; therefore, vertical metrics must remain uncompressed.

- **Typeface Selection**: `Noto Sans` (with primary runtime fallback to `Noto Sans Kannada`). It provides open counters, robust stroke terminals, and pristine rendering across Android OS releases.
- **Line Heights**: Kept at an ample `1.5` to `1.65` ratio across all scales to prevent overlapping diacritics and ligatures.
- **Scale Strategy**: Minimum body size never drops below `16px` on mobile devices. Font sizes smaller than `13px` are strictly prohibited to maintain legibility for users with early presbyopia working without reading glasses in the field.

## Layout & Spacing

The layout follows a fluid single-column model on mobile devices (width < 600px) expanding into a constrained 4-to-8 column structure on tablets and desktop terminals. 

- **Canvas Boundaries**: Outer horizontal padding is fixed to `16px` (`margin-mobile`) on phones to maximize the horizontal run for Kannada text strings, avoiding awkward hyphenations or line breaks in compound words.
- **Vertical Rhythm**: Layout components stack rhythmically using `space-md` (`16px`) and `space-lg` (`24px`).
- **Touch Safe Zones**: Interactive zones are spaced apart by at least `12px` to prevent accidental taps from wet, soil-stained, or calloused fingers.
- **Max Content Width**: On wider tablet or desktop screens, content containers constrain at `640px` for advisory reading flows and `840px` for multi-card dashboard overviews, maintaining a comfortable line length.

## Elevation & Depth

This design system avoids blurry, low-contrast box shadows, which degrade into muddy patches under outdoor glare and budget TN/IPS smartphone displays.

- **Tonal Layering**: Depth is achieved entirely through structured color containers. The base canvas (`#FAFAF6`) hosts elevated surface containers (`#EAF4EC` or `#FFFFFF`).
- **Crisp Structural Boundaries**: Every card, sheet, and advisory container uses a `1px` or `1.5px` solid border (`#D2E2D6`). 
- **Active State Elevation**: Pressed states do not rise; they shift into deeper tinted tones (e.g., `#216B45` darkens to `#174D32`, and `#EAF4EC` deepens to `#D6E8D9`).
- **Modal Sheets**: Overlays use a solid 40% backdrop tint (`#26352C` at 0.40 alpha) accompanied by a distinct 2px top border on the bottom sheet, completely bypassing drop shadow reliance.

## Shapes

The geometry uses balanced, approachable radii to convey friendliness and comfort while maintaining institutional reliability.

- **Primary Action Elements**: Buttons, text input containers, and audio-advisory bars use a `12px` to `16px` radius (`rounded-lg`), creating an approachable, tactile shape that is clearly pressable.
- **Content Cards & Panels**: Paddy health alerts, weather modules, and mandi price blocks use `16px` to `20px` corners, cleanly distinguishing them from outer page boundaries.
- **Badges & Pills**: Status pills (such as "Watering Due" or "Thriving") use a pill format (`rounded-full` / `9999px`) to immediately signal categorical status rather than interactive card panels.

## Components

### Buttons
- **Touch Target**: Strict minimum height of `52px` (optimal `56px`), with full-width orientation on mobile viewports.
- **Primary Button**: Solid `#216B45` background, `#FFFFFF` text (`label-lg`), with `14px` border radius. 
- **Secondary Button**: `#EAF4EC` background, `#216B45` text, bounded by a `1.5px` border in `#216B45`.
- **Audio Assist Action**: High-priority pill button containing an inline speaker icon (24px) alongside large text ("ಸಲಹೆ ಕೇಳಿ" / "Listen to Advice"), surfaced in `#216B45` with `#FAFAF6` text.

### Advisory Cards
- **Structure**: Surface fill in `#FFFFFF` or `#EAF4EC`, bounded by a `1.5px` solid `#D2E2D6` outline. Corner radius set to `18px`.
- **Padding**: Inner padding set uniformly to `20px`.
- **Hierarchy**: Header row hosts a status pill and date/time timestamp in `#4F6355`. Headline follows in `headline-md` (`#26352C`), with supporting steps in `body-md`.

### Status Badges
- **Thriving / Normal**: `#EAF4EC` surface with `#216B45` text and 1px `#216B45` stroke.
- **Caution / Water-Pest Warning**: `#FEF4E6` surface with `#B46B08` text, bounded by a 1px solid `#E8A23A` stroke.
- **Canal / Info Alert**: `#EBF3FA` surface with `#2B6CB0` text, bounded by a 1px solid `#90CDF4` stroke.
- **Typography & Form**: `label-sm` bold, all-caps or native Kannada conjuncts, pill-shaped radius (`9999px`), internal padding `6px 14px`.

### Input Fields
- **Height**: Minimum `56px` to facilitate effortless typing in field environments.
- **Styling**: Background `#FFFFFF`, border `2px` solid `#D2E2D6`, text `#26352C` in `body-lg`. Focus state shifts the border to `#216B45` with no outer glow.
- **Supporting Labels**: Floating or persistent top labels in `label-md` (`#26352C`), with explicit placeholder examples in Kannada.

### Checkboxes & Radio Selection
- **Dimension**: Hit box of `48px × 48px` enclosing a `26px × 26px` visual control to prevent mis-selection.
- **Border**: `2px` solid `#4F6355`; checked state fills with `#216B45` and renders a clean `#FFFFFF` tick mark with a 3px stroke weight.

### Iconography
- **Specifications**: Monoline icons drawn with a uniform `2px` stroke weight, rounded caps, and corners. 
- **Dimensions**: Standard base size `24px × 24px`, scaling to `32px × 32px` for quick-action navigation bars. Never use thin hairline strokes.