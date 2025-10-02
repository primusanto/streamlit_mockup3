# Design Language

This dashboard uses a brand-inspired design language with clean, premium aesthetics.

## Color Palette

### Primary Colors
- **Broom Yellow** (#ffe512) - Primary accent color, used for highlights and key UI elements
- **Scorpion Gray** (#595959) - Primary text color and dark elements
- **Ecru White** (#FAF9F2) - Main background color

### Secondary Colors
- **Darker Yellow** (#d4b000) - Secondary accent for variety
- **Deep Green** (#2d5f3f) - Success indicators
- **Amber** (#e8a317) - Warning indicators
- **Deep Red** (#8b3a3a) - Danger/negative indicators
- **Medium Gray** (#7a7a7a) - Neutral elements
- **Light Gray** (#d4d4d0) - Comparison/secondary data

### Chart Colors
Yellow-based gradient palette:
- #ffe512 (Brightest yellow)
- #d4b000 (Dark yellow)
- #b89f00 (Darker)
- #9e8700 (Darker still)
- #856f00 (Deep)
- #6b5800 (Deepest)

## Typography

### Headings
**Font:** Playfair Display (Serif)
- Elegant, professional serif font
- Used for: Dashboard title, section headers, KPI values
- Weights: 400, 600, 700, 800

### Body Text
**Font:** Lato (Sans-serif)
- Clean, highly readable sans-serif
- Used for: All body text, labels, data tables
- Weights: 300, 400, 700, 900

## Design Principles

### 1. Clean & Minimal
- Subtle shadows (0 1px 3px rgba)
- Simple borders (1-3px solid)
- Minimal border-radius (4px)
- White space for breathing room

### 2. Professional & Premium
- Elegant serif headings (Playfair Display)
- Clean sans-serif body (Lato)
- Muted color palette
- Subtle hover effects

### 3. Visual Hierarchy
- **Yellow accent** draws attention to important elements
- **Typography contrast** between headings and body
- **Card elevation** through subtle shadows
- **Color coding** for data visualization

### 4. Consistency
- Uniform spacing (0.5rem, 1rem, 1.5rem, 2rem)
- Consistent border styles
- Repeated card patterns
- Unified chart styling

## UI Components

### KPI Cards
```css
- Background: White (#ffffff)
- Border-top: 3px solid Yellow (#ffe512)
- Shadow: 0 1px 3px rgba(89, 89, 89, 0.12)
- Border-radius: 4px
- Hover: Elevates with stronger shadow
```

### Dashboard Header
```css
- Background: White (#ffffff)
- Border-bottom: 3px solid Yellow (#ffe512)
- Title: Playfair Display, 2.5rem, Gray (#595959)
- Subtitle: Lato, 1rem, Medium Gray (#7a7a7a)
```

### Tabs
```css
- Border-bottom: 1px solid Light Gray (#e5e5e0)
- Active tab: Yellow bottom border (#ffe512)
- Hover: Darker yellow (#d4b000)
- Font: Lato, 600 weight
```

### Sidebar
```css
- Background: White (#ffffff)
- Border-right: 1px solid Light Gray (#e5e5e0)
- Labels: Lato, 600 weight
- Headers: Playfair Display, 700 weight
```

### Charts
```css
- Background: White containers
- Font: Lato for labels, Playfair Display for titles
- Colors: Yellow-based palette
- Grid: Subtle gray lines
```

### Buttons
```css
- Background: Yellow (#ffe512)
- Text: Gray (#595959)
- Hover: Darker Yellow (#d4b000)
- Font: Lato, 700 weight
```

## Interaction States

### Hover Effects
- **Cards**: Subtle lift (translateY(-2px)) + shadow increase
- **Tabs**: Color change + border color change
- **Buttons**: Background darkens + lift effect
- **Expanders**: Background tint + border color change

### Transitions
- All transitions: 0.2s ease
- Smooth, professional feel
- No jarring changes

## Spacing System

### Padding/Margin Scale
- **XS**: 0.5rem (8px)
- **SM**: 0.75rem (12px)
- **MD**: 1rem (16px)
- **LG**: 1.5rem (24px)
- **XL**: 2rem (32px)
- **2XL**: 2.5rem (40px)

### Consistent Application
- Card padding: 1.5rem
- Header padding: 2rem 2.5rem
- Section margins: 2rem top, 1.25rem bottom
- Content gaps: 1rem - 1.5rem

## Accessibility

### Color Contrast
- Text on white: Gray (#595959) - WCAG AA compliant
- Yellow accents: Used for non-text elements or with sufficient contrast
- Chart colors: Distinguishable for colorblind users

### Typography
- Minimum font size: 0.75rem (12px)
- Line height: 1.1 - 1.5 for readability
- Letter spacing: Optimized for each font

### Interactive Elements
- Clear hover states
- Sufficient click targets
- Keyboard accessible (Streamlit default)

## Chart Design Guidelines

### Colors
1. Use yellow-based palette for primary data
2. Use gray (#d4d4d0) for comparison/secondary data
3. Use semantic colors for status (green/amber/red)

### Typography
- Titles: Playfair Display
- Labels/Axes: Lato
- Data labels: Lato

### Layout
- Clean backgrounds (transparent/white)
- Subtle gridlines
- Clear legends
- Appropriate spacing

### Specific Chart Types
- **Bar charts**: Yellow (#ffe512) primary, Gray (#d4d4d0) secondary
- **Line charts**: Yellow palette, area fills for emphasis
- **Donut charts**: Full yellow gradient palette
- **Arrears buckets**: Green → Amber → Orange → Red (severity gradient)

## Responsive Design

### Breakpoints (Streamlit default)
- Desktop: Full width (max 1400px)
- Tablet: Streamlit handles
- Mobile: Streamlit handles

### Adaptations
- Cards stack on smaller screens
- Charts resize responsively
- Sidebar collapsible
- Touch-friendly targets

## Best Practices

### Do's ✅
- Use white cards on ecru background
- Apply yellow accent sparingly
- Use Playfair for headings, Lato for body
- Maintain consistent spacing
- Keep shadows subtle
- Use semantic colors for data

### Don'ts ❌
- Don't use bright/neon colors
- Don't mix other font families
- Don't use heavy shadows or gradients
- Don't ignore the spacing system
- Don't use yellow for large text blocks
- Don't overcomplicate layouts

## Implementation Notes

### Font Loading
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Lato:wght@300;400;700;900&display=swap');
```

### Color Variables (config.py)
```python
PRIMARY_COLOR = "#ffe512"    # Broom Yellow
DARK_COLOR = "#595959"       # Scorpion Gray
LIGHT_COLOR = "#FAF9F2"      # Ecru White
SECONDARY_COLOR = "#d4b000"  # Darker Yellow
SUCCESS_COLOR = "#2d5f3f"    # Deep Green
WARNING_COLOR = "#e8a317"    # Amber
DANGER_COLOR = "#8b3a3a"     # Deep Red
```

### Streamlit Config
```toml
[theme]
primaryColor = "#ffe512"
backgroundColor = "#FAF9F2"
secondaryBackgroundColor = "#ffffff"
textColor = "#595959"
font = "sans serif"
```

## Design Evolution

This design language is inspired by professional real estate branding with:
- Clean, premium aesthetic
- Elegant typography pairing (serif + sans-serif)
- Subtle, sophisticated color palette
- Focus on readability and data clarity
- Professional, executive-ready appearance

The yellow accent provides energy and optimism while maintaining professionalism through restrained application and pairing with muted grays and whites.
