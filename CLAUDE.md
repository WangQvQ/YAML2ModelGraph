# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

YAML2ModelGraph converts Ultralytics YOLO YAML model configuration files into SVG architecture diagrams. It parses `backbone:` and `head:` sections from YOLO YAML files, identifies module types (Conv, C2f, Concat, Detect, Upsample, etc.), and renders a three-lane SVG diagram (Backbone → Neck → Head) with colored nodes, type-strips, and connection paths.

## Commands

```bash
# Install dependency
pip install pyyaml

# Generate SVG with default theme (paper), single Detect head
python main.py examples/yolo26.yaml output.svg

# Generate SVG with a specific theme
python main.py examples/yolo26.yaml output.svg --theme dark

# Generate with 3 separate Detect heads (P3/8, P4/16, P5/32)
python main.py examples/yolo26.yaml output.svg --head multi

# Available themes: paper, candy, dark, ocean, retro, blueprint, forest, paper_ryb, journal
# --head: single (default, one Detect node) or multi (one Detect node per scale)
```

There are no tests, linter configs, or build steps. The project has no packaging — it's run as a script.

## Architecture (3 files)

**`main.py`** — CLI entry point. Parses sys.argv, defines `DISPLAY_CONFIG` (controls which metadata appears on nodes), loads theme via `themes.get_config()`, calls `yolo_graph.parse_and_layout()`.

**`themes.py`** — Theme registry. `DEFAULT_LAYOUT` holds base layout constants (lane widths, node dimensions, step sizes, column gaps). Each theme dict provides `colors`, `gradients`, `type_colors`, `font`, and optional `radius`. `get_config(name)` merges `DEFAULT_LAYOUT` with the chosen theme. To add a theme: define a new dict, register it in the `THEMES` dict.

**`yolo_graph.py`** — Core logic. Two components:
- `SVGBuilder` class: low-level SVG primitives (rects with gradient fills + type-color strips, background lanes, connection paths with 4 routing strategies: `vertical_straight`, `manhattan`, `detour_right`, `standard`).
- `parse_and_layout()` function: the main pipeline — (1) parse YAML into layer metadata (type, channels, stride, sources), (2) assign lanes (backbone=col 0, neck=col 1, Detect=col 2), (3) layout positions (backbone vertical, neck multi-column folding up to 3 columns, head aligned to source averages or bottom-stacked in multi-head mode), (4) route connections, (5) write SVG.

## Key Design Details

- **Channel tracking**: `layer_channels` dict tracks per-layer channel counts. `Concat` sums input channels; `Upsample` is channel-passthrough.
- **Stride tracking**: Conv with stride=2 doubles stride; Upsample halves it. Used for sub-labels like `/32x`.
- **Module type coloring**: Only `Conv`, `Concat`, `Detect`, `Upsample`, and `C2f` have dedicated `type_colors` entries. All other modules (C3k2, A2C2f, SPPF, etc.) fall through to the `"Other"` color. This is defined in each theme's `type_colors` dict.
- **Neck column folding**: When neck nodes exceed `max_bb_y`, layout spills into a second column (max 3 columns via `neck_cols_layout`).
- **DISPLAY_CONFIG** in `main.py` controls which fields appear on nodes: `show_channels`, `show_repeats`, `show_stride`, `show_args`. `show_args` defaults to `False` to avoid text overflow.
- **SVG output directory**: `svg/` holds single-head examples (one per theme), `svg/multi/` holds triple-head examples. Both are generated from `examples/yolo26.yaml`.
