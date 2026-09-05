# THE HOUSE ON MERCER LANE
## Complete Art Direction & Asset Production Guide
### Solo Developer Edition — PS1/PS2 Aesthetic

---

## 1. THE VISUAL IDENTITY IN ONE SENTENCE

A 90s American working-class rental home rendered in PS1-era lo-fi — warm and readable in Loop One, progressively drained and wrong by Loop Three, with the degradation feeling like a memory losing fidelity rather than a haunting gaining intensity.

---

## 2. THE AESTHETIC TARGET

### What "PS1 Style" Actually Means (Technically)

PS1 style is not just low poly. It's a specific combination of constraints that create a recognizable look. Hit all of these and the aesthetic is coherent. Miss one and it reads as "cheap indie" instead of "intentional retro."

| Parameter | PS1 Target | PS2 Target | Mercer Lane Target |
|-----------|-----------|-----------|-------------------|
| Polygon count per room | 500-1500 tris | 2000-5000 tris | 1500-3000 tris |
| Polygon count per prop | 50-200 tris | 200-800 tris | 100-400 tris |
| Texture resolution | 64x64 to 256x256 | 256x256 to 512x512 | 128x128 to 256x256 |
| Texture filtering | None (pixelated) | Bilinear | None — keep pixels sharp |
| Color depth appearance | Dithered, banded | Smoother | Dithered (shader handles this) |
| Vertex snapping | Yes (wobbly geometry) | Less | Optional — adds authenticity |

**The Mercer Lane sweet spot is early PS2 resolution with PS1 texture filtering.** Geometry is clean enough to read clearly (Loop One) but textures are low-res and pixelated. The FlashbackManager shader your prototype already has handles dithering and chromatic aberration — that's most of the aesthetic work done in code.

### Reference Games (Study These)

- **Silent Hill (PS1)** — fog use, color desaturation technique, how domestic spaces become wrong
- **Resident Evil 2 (PS1)** — how to make a police station feel real at low poly counts
- **Clock Tower (PS1)** — domestic horror, single house, how rooms feel lived-in with minimal geometry
- **Haunting Ground (PS2)** — closest to Mercer Lane's tone; a house that feels real and wrong
- **Rule of Rose (PS2)** — color palette reference; how to make warm feel oppressive

---

## 3. COLOR PALETTE — ALL THREE LOOPS

This is the most important design decision in the document. The palette does 60% of the emotional work. Get this right and average geometry still feels intentional. Get it wrong and perfect geometry still feels off.

### Loop One — "Just Another Night"
*Warm. Domestic. Trying to look like home.*

```
Primary Warm:     #C4956A  — wood paneling, furniture surfaces
Kitchen Light:    #E8C882  — the overhead kitchen fluorescent spill
Shadow Base:      #2C1F14  — dark corners, under furniture
Carpet Brown:     #7A5C3E  — the carpet that exists in every 90s rental
Wall Paint:       #D4C4A8  — off-white walls, slightly yellow from age
Linoleum Grey:    #8A8070  — kitchen/bathroom floor
TV Static:        #F0EDE8  — the living room lit by TV glow
Accent Rust:      #8B4513  — Ray's bottles, worn wood edges
```

### Loop Two — "Something Is Wrong"
*The warmth is pulling back. Cooler tones bleed in.*

Same palette, but in Godot's WorldEnvironment:
- Reduce `ambient_light_energy` by 20%
- Shift color grade toward blue-grey: `#B8C4C8` tint
- Increase contrast slightly — shadows get darker, highlights stay

Specific changes to materials:
- Wood paneling desaturates: `#A87D5A` (from `#C4956A`)
- Wall paint goes cooler: `#C8BFAF` (from `#D4C4A8`)
- Kitchen light dims and yellows: `#D4AE60` (from `#E8C882`)

### Loop Three — "The Truth"
*Near-monochrome. Two colors survive at full saturation.*

Global desaturation via shader: 85-90% grey
**Exceptions — these two colors stay vivid at all times:**
- Leo's red-and-white shirt: `#CC2222` / `#F0EDE8` — always the brightest object in frame
- VCR clock green: `#00FF41` — the only light in the living room that doesn't change

Everything else:
- Wood paneling: `#5A5048`
- Walls: `#8A8480`
- Shadows: `#1A1818`
- Kitchen light: OFF or near-off `#2A2820`

**Sandra's arrival (ending):** One warmth color returns — the amber of the living room light bleeding down the basement stairs. `#C4956A` — the same Primary Warm from Loop One. It comes from above. From where she is. It's the only warm light in the basement.

### Basement (Loop Three Only)
The basement doesn't follow the loop palette — it has its own:
```
Concrete Floor:   #4A4440  — raw, cold
Stone Wall:       #3C3835  — darker than upstairs
Single Bulb:      #D4AE60  — warm but isolated, casts hard shadows
Deep Shadow:      #0F0E0D  — near-black in corners
```

---

## 4. THE HOUSE — ROOM-BY-ROOM LAYOUT

### Floor Plan (Top-Down Schematic)

```
SECOND FLOOR:
┌─────────────────────────────────┐
│                                 │
│  LEO'S      │  BATH  │  RAY +  │
│  BEDROOM    │        │  SANDRA │
│  (small)    │        │  ROOM   │
│             │        │  (door  │
│             │        │  never  │
│             │        │  opens) │
│─────────────────────────────────│
│         UPSTAIRS HALLWAY        │
│     (narrow — 1.2m wide)        │
└─────────────────────────────────┘

FIRST FLOOR:
┌─────────────────────────────────┐
│                                 │
│    LIVING ROOM                  │
│    (largest room)               │
│    TV / Couch / Window          │
│                                 │
│─────────────────────────────────│
│  KITCHEN       │  SMALL         │
│  (linoleum)    │  HALLWAY       │
│  Fridge/Stove  │  (basement     │
│  Table/counter │   door here)   │
│                │                │
└─────────────────────────────────┘

BASEMENT (accessed via hallway door):
┌─────────────────────────────────┐
│  STAIRS (7 steps down)          │
│                                 │
│  Storage area                   │
│  Boxes / Fishing gear           │
│  Single bulb pull-string        │
│                                 │
│  [Leo's body — far corner]      │
└─────────────────────────────────┘
```

### Room Dimensions (in Godot units, 1 unit = 1 meter)

| Room | Width | Depth | Height | Notes |
|------|-------|-------|--------|-------|
| Living Room | 5.5m | 4.5m | 2.4m | Largest room, feels spacious then oppressive |
| Kitchen | 3.5m | 4.0m | 2.4m | Linoleum, drop ceiling feel |
| Hallway (ground) | 1.4m | 2.5m | 2.4m | Tight — basement door at end |
| Upstairs Hallway | 1.2m | 4.0m | 2.2m | Narrow on purpose — Ray's door looms |
| Leo's Bedroom | 2.8m | 3.2m | 2.2m | Small. Child-scale everything |
| Bathroom | 1.8m | 2.4m | 2.2m | Smallest room |
| Ray/Sandra Bedroom | 3.5m | 3.8m | 2.2m | Door never opens |
| Basement | 5.0m | 5.5m | 2.0m | Low ceiling. Oppressive. |

**Critical design note:** The camera is at 0.85m height (Leo's eye level). Design every room from that height. The kitchen counter should be at Leo's chin. Doorknobs at his eye level. The couch should be a wall of fabric from his perspective. Test every room by crouching in Godot's editor viewport to Leo-height before finalizing geometry.

---

## 5. ROOM-BY-ROOM ASSET LIST

### Priority order: build in this sequence. Each room unlocks testing of the loop system.

---

### ROOM 1: LIVING ROOM (Build First)

**Architecture (CSG in Godot — build these yourself):**
- Floor — wood planks, scratched. Texture: 256x256 horizontal grain
- Walls — wood paneling lower half, painted drywall upper half. Two textures meeting at a horizontal seam at 1.0m height
- Ceiling — plain, slightly yellowed
- One window (front wall) — simple frame, no glass mesh needed, just emit the street light color through it

**Props (model in Blender or AI-generate):**

| Prop | Poly budget | Notes |
|------|-------------|-------|
| CRT Television (tube TV) | 200 tris | The most important prop in the game. Boxy. Big back. Wood-grain sides. |
| Particle-board TV stand | 80 tris | Cheap. Sagging slightly |
| Couch (3-seater, worn) | 300 tris | Floral or plain. 90s rental couch. Not a sofa — a couch. |
| Coffee table | 60 tris | Scratched surface, ring stains (in texture) |
| VCR (on TV stand) | 80 tris | Clock display: green LED. This is a separate emissive mesh |
| Family photo frame (wall) | 30 tris | Flat quad with frame edge. Photo is a texture. |
| Carpet (area rug) | 8 tris | Flat plane with tiling carpet texture |
| Loose floorboard (near hallway) | 4 tris | Slightly raised plane, same wood texture |
| Window curtains | 60 tris | Simple folds. Thin mesh. |
| Lamp (floor or table) | 80 tris | Warm light source — point light attached |

**Textures needed:**
- `wood_planks_scratched_256.png` — floor
- `wood_paneling_256.png` — lower wall
- `wall_paint_offwhite_256.png` — upper wall
- `carpet_brown_128.png` — tiling carpet texture
- `tv_screen_static.png` — animated or scrolling noise (can use shader)
- `family_photo_normal.png` / `family_photo_loop2.png` / `family_photo_loop3.png` — three versions

---

### ROOM 2: KITCHEN (Build Second)

**Architecture:**
- Floor — linoleum. Checkerboard or worn solid pattern. 128x128 tiling
- Walls — painted drywall, slightly different color from living room
- Drop ceiling suggestion — slightly lower ceiling height (2.2m vs 2.4m) + strip light fixture

**Props:**

| Prop | Poly budget | Notes |
|------|-------------|-------|
| Refrigerator (90s style) | 180 tris | White. Rounded corners. Handle on right side |
| Gas stove/oven | 200 tris | White or off-white. Pot sitting on it |
| Kitchen counter | 100 tris | Laminate top, wood-veneer cabinet below |
| Kitchen sink | 120 tris | Double basin. Chrome tap. This tap drips — particle emitter |
| Kitchen table | 80 tris | 4-person. Scratched laminate top |
| Two chairs (mismatched) | 60 tris each | Different styles — the family didn't buy these together |
| Cereal box (on counter) | 40 tris | Generic design, bright color |
| Cereal bowl (on counter) | 30 tris | Half-eaten in Loop 1, empty in Loop 2+ |
| Pot (on stove) | 60 tris | With lid |
| Fridge note | 8 tris | Flat quad stuck to fridge door |
| Medicine bottles (counter) | 20 tris each | Small pill bottles, visible in Loop 2+ |
| Calendar (wall) | 8 tris | Flat quad, texture with month visible |
| Overhead light fixture | 40 tris | Strip fluorescent. Important light source |
| Back door | 80 tris | Hollow-core door. Locked. |

---

### ROOM 3: UPSTAIRS HALLWAY (Build Third — needed for Loop Two)

**Architecture:**
- Narrow. 1.2m. Deliberately tight.
- Wood floor (same texture as living room but different color grade)
- Painted walls — same off-white but more scuffed
- Two doors: Leo's bedroom (opens), Ray's bedroom (never opens)
- Bathroom door (opens)

**Props:**

| Prop | Poly budget | Notes |
|------|-------------|-------|
| Ray's bedroom door | 100 tris | Closed. Light under it in Loop 2 — emissive strip on floor |
| Door (generic, 2x) | 100 tris each | Leo's room + bathroom |
| Framed wedding photo | 30 tris | On hallway wall. Visible from hallway. |
| Ray's work boots (floor) | 80 tris | By the wall near Ray's door |
| Light fixture (ceiling) | 30 tris | Bare bulb. Flickers in Loop 2. |

---

### ROOM 4: LEO'S BEDROOM (Build Fourth)

**The most emotionally dense room. Every object matters.**

**Props:**

| Prop | Poly budget | Notes |
|------|-------------|-------|
| Child's bed (single) | 150 tris | Low to ground. Blanket/pillow in texture |
| Reg the rabbit (on pillow) | 80 tris | Stuffed animal. Soft-looking. Worn. |
| Small dresser | 100 tris | 3 drawers. Cheap. |
| Shelf (wall-mounted) | 40 tris | Piggy bank + miscellaneous |
| Piggy bank | 40 tris | Ceramic. Pink or blue. Plug visible. |
| Rocket/astronaut poster | 8 tris | Flat quad on wall |
| Box under bed | 60 tris | Cardboard. Flaps closed. Interactable in Loop 3. |
| Child's drawings (wall) | 8 tris each x3 | Flat quads. Different drawings per loop. |
| Window | 60 tris | Looking out to street. Important — Leo watches for headlights here |
| Small desk or toy chest | 80 tris | Optional. Adds life to room. |

---

### ROOM 5: BATHROOM (Build Fifth)

**Small room. Three key props.**

| Prop | Poly budget | Notes |
|------|-------------|-------|
| Toilet | 120 tris | White. 90s style. |
| Sink/vanity | 100 tris | Mirror above it — THIS IS KEY. See mirror section below. |
| Bathtub | 150 tris | Cast iron look or plastic. Shower curtain rod + curtain |
| Medicine cabinet | 60 tris | Above or beside sink. Opens in Loop 2 |
| Cracked floor tile | 0 tris | Texture detail on floor — mark one tile with crack in texture |

**The Mirror — Special Case:**
The mirror in Loop 3 shows a delayed reflection. In Godot 4, implement with a `SubViewport` rendering the scene from a Camera3D positioned at the mirror surface, with a 0.5-second delay achieved by storing frames. Alternatively: swap the mirror material to a slightly desaturated texture of the room — cheaper, still effective, easier to implement solo.

---

### ROOM 6: BASEMENT (Build Last — only needed for Loop Three)

**The most important room. Least time to get right.**

| Prop | Poly budget | Notes |
|------|-------------|-------|
| Concrete stairs (7 steps) | 80 tris | Each step is a trigger zone |
| Pull-string light bulb | 30 tris | Hanging. String visible. Emissive when on. |
| Storage boxes (stacked) | 40 tris each x6 | Various sizes. Sandra's "BEFORE" box is distinct. |
| Fishing box | 60 tris | Plastic tackle box. Weathered. |
| Single child's shoe | 20 tris | Tiny. Under the stairs. |
| Leo's body | 200 tris | Static mesh. Red-white striped shirt. This is a crucial asset — spend time on it. |
| Old furniture (covered) | 100 tris | Sheet-covered shapes in background |
| Exposed pipe (ceiling) | 30 tris | Adds authenticity. Dripping pipe option. |

---

## 6. TEXTURE PRODUCTION GUIDE

### The Rules

1. **All textures: power of 2.** 64, 128, 256. Never 300x200. Godot will warn you.
2. **No filtering.** In Godot, set every texture import to `Filter: Nearest`. This keeps pixels sharp and gives the PS1 look.
3. **No mipmaps** on most textures. Or set mipmap filter to `Nearest` too.
4. **Tiling textures:** floors, walls, carpet — make these seamless and tile them. Don't use one huge texture for a floor.
5. **Color count:** PS1 textures had 16 or 256 colors. You don't need to enforce this strictly, but keep your textures low-saturation and avoid gradients. Flat color areas with hand-painted noise look right.

### In Godot — Import Settings (Set These for Every Texture)
```
Compress Mode: Lossless
Filter: Nearest
Mipmaps: Off (or Nearest)
Repeat: Enabled (for tiling textures)
```

### How to Make Textures (Three Methods)

**Method 1: Paint in Krita or Aseprite (Recommended)**
- Aseprite is built for pixel art — $20, worth every cent for this workflow
- Work at 128x128 or 256x256 canvas
- Use a limited palette (pull from the color palette section above)
- Export as PNG

**Method 2: Photo-based (Fast)**
- Find a reference photo of wood paneling, linoleum, carpet
- Open in Photoshop/GIMP
- Image → Mode → Indexed Color → 32 colors (posterizes it)
- Scale to 256x256
- Make it seamless: Filter → Other → Offset, clone-stamp the seams
- Export PNG

**Method 3: AI-generated textures (Fastest)**
- Use [Poly Haven](https://polyhaven.com) — free PBR textures, download and downscale
- Or generate with [Stable Diffusion + seamless tile prompt]
- Downscale to 256x256 in Photoshop
- Reduce colors to 32-64 with posterize
- The pixelation IS the aesthetic

### Textures to Make First (Priority Order)

1. `wood_planks_scratched_256.png` — used in living room and upstairs
2. `wall_paint_offwhite_256.png` — used everywhere upstairs
3. `wood_paneling_256.png` — living room lower walls
4. `linoleum_tile_128.png` — kitchen floor (tiling 2x2 pattern)
5. `carpet_brown_128.png` — living room area rug
6. `concrete_rough_256.png` — basement floor and walls

---

## 7. BLENDER WORKFLOW — PS1 ASSETS

### Setup (Do This Once)

1. **Blender Units:** Set scene unit to Meters. 1 Blender unit = 1 Godot unit = 1 meter.
2. **Overlay Grid:** Set grid scale to 0.1 so you can snap to 10cm increments
3. **Polygon budget display:** Enable Statistics overlay (Viewport Overlays → Statistics) — watch your tri count as you model
4. **Export format:** glTF 2.0 (.glb) — Godot imports this natively, best format for this pipeline

### Modeling Approach for PS1/PS2 Style

**Start boxy. Stay boxy.**

PS1 assets are not low-detail versions of high-detail models. They are objects designed from the start to read at low poly counts. A PS1 couch is 6-10 rectangles arranged to suggest a couch — not a couch with detail removed.

**The Process (for any prop):**
1. Start with a cube
2. Scale it to real-world proportions (a couch is roughly 2m wide, 0.9m tall, 0.8m deep)
3. Add the minimum faces needed to read as the object — usually 2-4 loop cuts
4. Add a tiny bevel (0.02m) on hard edges — this catches light and stops edges from looking like paper
5. Unwrap UV (Smart UV Project works fine for boxy objects)
6. Assign a single 256x256 texture
7. Hand-paint or project the texture in Blender's texture paint mode
8. Export as .glb

**Poly counts to target:**

| Object type | Target tris | How to think about it |
|-------------|-------------|----------------------|
| Large furniture (couch, fridge) | 150-300 | A fridge is basically a box with a door |
| Medium furniture (table, chair) | 60-120 | A table is 5 boxes |
| Small props (bottle, bowl) | 20-60 | A bottle is a cylinder with 6 sides |
| Architecture (walls, floor) | 8-20 per section | Flat planes. Keep it flat. |
| Character body (Leo, Sandra silhouette) | 300-600 | Simple humanoid, no fingers |

### Lighting in Godot (Not Blender)

Do not bake lighting into textures for this game. Light everything in Godot using:

- **OmniLight3D** — for lamps, the TV glow, the basement bulb
- **DirectionalLight3D** — one per scene for ambient directional (soft, low intensity)
- **WorldEnvironment** — ambient light color (this shifts per loop via the palette system)

The FlashbackManager shader already handles the visual degradation between loops. The lighting shift is handled by tweening `WorldEnvironment` ambient light color and energy in `House.gd` when `loop_changed` fires.

---

## 8. AI TOOL PIPELINE (For What You Can't Model)

### Recommended Tools

**For 3D generation:**
- **Meshy.ai** — best for furniture and props. Upload a reference image or text prompt. Downloads as .obj or .glb. Then bring into Blender, reduce poly count with Decimate modifier, re-UV, retexture.
- **Tripo3D** — similar to Meshy. Try both on the same prompt and pick the better result.
- **CSM (Common Sense Machines)** — image-to-3D. Take a photo of a real 90s couch and it generates a 3D version.

**Workflow for AI-generated assets:**
1. Generate in Meshy/Tripo
2. Import .glb into Blender
3. Decimate modifier → target poly count (see table above)
4. Re-UV with Smart UV Project
5. Create a new 256x256 texture
6. Texture Paint in Blender — paint over the AI texture with your palette colors
7. Export .glb
8. Import into Godot, set texture filter to Nearest

**The key step is step 6.** AI-generated textures are photorealistic and high-res — they will not look PS1 unless you repaint them in your palette. 20 minutes of texture painting per asset transforms it from "AI slop" to "intentional retro."

### What to AI-Generate vs Model Yourself

| Asset | Method | Why |
|-------|--------|-----|
| CRT Television | Model in Blender | Iconic prop — needs to be right |
| Couch | AI generate | Complex organic shape, hard to model well |
| Fridge | Model in Blender | It's a box — faster to model than AI workflow |
| Stove | AI generate | Details are fiddly, AI handles them |
| Stuffed rabbit (Reg) | AI generate | Organic shape |
| Boxes/containers | Model in Blender | Literal boxes — 2 minutes each |
| Toilet/bathtub | AI generate | Organic curves |
| Leo's body (static mesh) | Model in Blender | Too important to trust to AI |

---

## 9. GODOT SCENE SETUP — LOOP PALETTE SYSTEM

This is how the color palette shifts between loops in code, without duplicating assets.

### WorldEnvironment Per Loop

Create one `WorldEnvironment` node in your house scene. Attach this script:

```gdscript
# HousePalette.gd
extends WorldEnvironment

func _ready():
    GameState.phase_changed.connect(_on_phase_changed)
    _apply_loop_palette(GameState.get_loop_number())

func _on_phase_changed(_phase):
    _apply_loop_palette(GameState.get_loop_number())

func _apply_loop_palette(loop: int) -> void:
    var tween = create_tween()
    tween.set_parallel(true)

    match loop:
        1:  # Warm, domestic
            tween.tween_property(environment, "ambient_light_color",
                Color(0.77, 0.58, 0.42), 1.5)  # #C4956A
            tween.tween_property(environment, "ambient_light_energy", 0.8, 1.5)
            tween.tween_property(environment, "adjustment_saturation", 1.0, 1.5)
            tween.tween_property(environment, "adjustment_brightness", 1.0, 1.5)

        2:  # Cooling, pulling back
            tween.tween_property(environment, "ambient_light_color",
                Color(0.72, 0.77, 0.78), 2.0)  # #B8C4C8
            tween.tween_property(environment, "ambient_light_energy", 0.6, 2.0)
            tween.tween_property(environment, "adjustment_saturation", 0.7, 2.0)
            tween.tween_property(environment, "adjustment_brightness", 0.9, 2.0)

        3:  # Near-monochrome
            tween.tween_property(environment, "ambient_light_color",
                Color(0.4, 0.4, 0.42), 2.5)
            tween.tween_property(environment, "ambient_light_energy", 0.3, 2.5)
            tween.tween_property(environment, "adjustment_saturation", 0.15, 2.5)
            tween.tween_property(environment, "adjustment_brightness", 0.8, 2.5)
```

### The Two Protected Colors (Loop Three)

Leo's shirt and the VCR clock must survive the desaturation. Handle this by:

1. Give Leo's shirt mesh its own `ShaderMaterial` with a simple unlit shader that ignores scene lighting and outputs `#CC2222` / `#F0EDE8` directly
2. VCR clock: emissive material, `emission_energy = 2.0`, `emission_color = #00FF41` — emissive ignores scene desaturation by default

---

## 10. ASSET BUILD ORDER (THE EXACT SEQUENCE)

Build in this order. Each step is testable before the next begins.

### Phase 1 — Blockout (Week 1-2)
**Goal: playable house with no art. Prove the layout works at Leo's eye height.**

1. Build all rooms using CSG nodes in Godot (boxes, no textures, grey)
2. Set player height to 0.85m, walk every room
3. Check: does the kitchen counter feel tall? Does Ray's door feel looming? Does the basement feel low and oppressive?
4. Adjust room dimensions until the scale feels right at child-height
5. Place all Proximity_trigger and ClickObject_trigger nodes — test the dialogue system end-to-end in grey-box
6. **Do not texture anything until layout is locked**

### Phase 2 — Living Room (Week 2-3)
**Goal: one complete room, full aesthetic.**

1. Make the 6 textures for the living room
2. Model or AI-generate the 10 living room props
3. Set texture import settings to Nearest filter
4. Set up WorldEnvironment Loop 1 palette
5. Screenshot from Leo's eye height — does it read as a 90s rental?

### Phase 3 — Kitchen + Hallway (Week 3-4)
**Goal: ground floor complete.**

### Phase 4 — Upstairs (Week 4-5)
**Goal: Leo's bedroom + bathroom + Ray's door sequence.**

### Phase 5 — Basement (Week 5-6)
**Goal: the climax sequence playable end-to-end.**

### Phase 6 — Loop 2 + 3 Material Variants (Week 6-7)
**Goal: palette shifts working, object state changes visible.**

### Phase 7 — Polish Pass (Week 7-8)
**Goal: lighting, particle effects (dripping tap), VCR clock emissive, TV static shader, door light leak under Ray's door.**

---

## 11. FREE RESOURCE LIST

### Textures (Free, Commercial OK)
- [Poly Haven](https://polyhaven.com) — best free PBR textures, downscale to 256
- [Texture Haven](https://texturehaven.com) — same collection
- [Lospec Palette List](https://lospec.com/palette-list) — for color palette reference and pixel art palettes

### 3D Assets (Free Starting Points)
- [Sketchfab Free](https://sketchfab.com/features/free-3d-models) — filter by low poly, check license
- [OpenGameArt](https://opengameart.org) — CC0 assets, some PS1-style packs exist
- [Quaternius](https://quaternius.com) — free low-poly packs, less cartoony than Kenney

### Blender Learning (Fastest Path)
- **Grant Abbitt** on YouTube — "Low Poly Character" and "Low Poly Modeling" series
- **Blender Guru** — "Donut tutorial" is for beginners but skip it, go straight to "Blender for Games" series
- For PS1 specifically: search "Blender PSX style tutorial" — several 20-minute tutorials cover the exact workflow

### Godot PSX Shader (Already Yours)
Your `flashback_shader.gdshader` handles most of the PSX post-processing. The additional shader you need is:
- A simple `psx_world.gdshader` applied to WorldEnvironment for vertex snapping (the wobbly geometry effect) — optional but adds authenticity

---

## 12. THE ONE RULE TO REMEMBER

**Design for Leo's eye height first. Everything else follows.**

At 0.85m, this house should feel enormous and slightly threatening even in Loop One. The couch back should be at his shoulder. The counter should be at his chin. The basement stairs should feel like a descent into something much larger than the upstairs suggests.

Every asset decision — how big, how detailed, how lit — runs through that lens first. If it doesn't feel right at 0.85m, it doesn't matter how good it looks in the editor at adult height.

---

*Art Direction Document v1.0 — THE HOUSE ON MERCER LANE*
*Solo Developer | PS1/PS2 Aesthetic | Godot 4*
