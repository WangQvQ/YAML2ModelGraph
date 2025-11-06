#!/usr/bin/env python3
"""
YAML -> Model Structure Graph (vertical layout, colored by module type)

Usage:
    python yml2modelgraph.py model.yaml [out_name] [--format svg|png]

Outputs:
    out_name.svg (default) or out_name.png

Dependencies:
    pip install pyyaml graphviz
    and install system graphviz (dot)
"""

import yaml
from graphviz import Digraph
import math
from typing import List, Any, Dict, Tuple
import sys
import os
import random


# ---------------- utils ----------------
def make_divisible(v, divisor=8):
    """Align v to nearest multiple of divisor (ceil)."""
    if v is None:
        return None
    return int(math.ceil(float(v) / divisor) * divisor)


def safe_eval(x):
    """Try to evaluate strings like '3' -> 3, '[1,2]' -> list, else keep original."""
    if not isinstance(x, str):
        return x
    try:
        return eval(x)
    except Exception:
        return x


def module_name_lower(m_raw):
    """Return module name in lowercase for heuristic checks."""
    if isinstance(m_raw, str):
        return m_raw.lower()
    try:
        return m_raw.__name__.lower()
    except Exception:
        return str(m_raw).lower()


# ---------------- color palette ----------------
def get_color_palette():
    """A set of visually distinct soft colors."""
    return [
        "#C2E7D9", "#FFD6A5", "#FFB5A7", "#A0C4FF", "#BDB2FF",
        "#B5E48C", "#FEC5BB", "#FCD5CE", "#D0F4DE", "#FFF0B3",
        "#A3C9A8", "#B8D0EB", "#E2B8A6", "#DDBDF1", "#B2F7EF"
    ]


# ---------------- parse model ----------------
def parse_yaml_model(d: Dict[str, Any], input_channels=3):
    """
    Parse ultralytics-like yaml into node list and edge list.
    Returns (layers, edges, backbone_len).
    """
    gd = float(d.get('depth_multiple', 1.0))
    gw = float(d.get('width_multiple', 1.0))
    seq_backbone = d.get('backbone', []) or []
    seq_head = d.get('head', []) or []
    seq = seq_backbone + seq_head

    ch = [input_channels]
    layers, edges = [], []

    for i, entry in enumerate(seq):
        if not (isinstance(entry, list) and len(entry) >= 4):
            continue
        f, n, m, args = entry
        from_idxs = [f] if isinstance(f, int) else list(f) if hasattr(f, "__iter__") else [f]
        try:
            n = int(n)
        except:
            n = 1
        args = [safe_eval(a) for a in (args or [])]
        group = "backbone" if i < len(seq_backbone) else "head"
        mname = module_name_lower(m)

        # --- input channels ---
        c1s = []
        for src in from_idxs:
            if isinstance(src, str):
                try:
                    src = int(src)
                except:
                    src = -1
            if src == -1:
                c1s.append(ch[-1])
            else:
                mapped = src + 1
                c1s.append(ch[mapped] if 0 <= mapped < len(ch) else ch[-1])

        # --- output channels ---
        if "concat" in mname:
            c2 = sum(c1s)
        else:
            c2 = args[0] if args and isinstance(args[0], int) else (c1s[0] if c1s else 0)
            if not ("detect" in mname):
                try:
                    c2 = make_divisible(c2 * gw)
                except:
                    pass
        n_ = max(round(n * gd), 1) if n > 1 else n

        # --- label ---
        if "detect" in mname:
            label_lines = [str(m), f"n={n_}", str(args)]
        else:
            label_lines = [str(m), f"{sum(c1s)} → {c2}", f"n={n_}"]
            if args:
                label_lines.append(str(args))
        label = "\\n".join(label_lines)
        layers.append({"idx": i, "group": group, "from": from_idxs, "label": label, "type": str(m)})
        ch.append(c2)

    # --- edges ---
    for node in layers:
        dst = node["idx"]
        for src in node["from"]:
            try:
                src_i = int(src)
            except:
                src_i = -1
            if src_i == -1:
                src_idx = dst - 1
            else:
                src_idx = src_i
            if src_idx < 0:
                src_idx = -999
            edges.append((src_idx, dst))
    edges = [(-1, dst) if src == -999 else (src, dst) for (src, dst) in edges]
    return layers, edges, len(seq_backbone)


# ---------------- graphviz drawing ----------------
def draw_graph(layers: List[Dict], edges: List[Tuple[int, int]], backbone_len: int,
               out_file="model_graph", fmt="svg"):
    dot = Digraph(comment="Model", format=fmt)
    dot.attr(rankdir="TB", splines="ortho", center="true")
    dot.graph_attr.update({"ranksep": "0.9", "nodesep": "0.5", "bgcolor": "white"})
    dot.attr(fontname="Helvetica", fontsize="10")

    dot.node("Input", "Input\\nC=3", shape="oval", style="filled", fillcolor="#FFDDAA")

    # assign color per module type
    palette = get_color_palette()
    type_colors = {}
    color_idx = 0
    for l in layers:
        t = l["type"]
        if t not in type_colors:
            type_colors[t] = palette[color_idx % len(palette)]
            color_idx += 1

    head_idx = layers[-1]["idx"] if layers else -1
    neck_layers = layers[backbone_len:-1] if backbone_len < len(layers) - 1 else []

    node_style_base = {
        "shape": "record",
        "style": "rounded,filled",
        "color": "#2F4F4F",
        "fontname": "Helvetica",
        "fontsize": "10"
    }

    # Backbone
    with dot.subgraph(name="cluster_backbone") as c:
        c.attr(label="Backbone", color="#c6e2ff", style="rounded",
               fontname="Helvetica", labelloc="t", labeljust="c", margin="20,20", rankdir="TB")
        for node in layers[:backbone_len]:
            node_style = node_style_base.copy()
            node_style["fillcolor"] = type_colors[node["type"]]
            c.node(f"L{node['idx']}", node["label"], **node_style)

    # Neck
    with dot.subgraph(name="cluster_neck") as c:
        c.attr(label="Neck", color="#fff0b3", style="rounded",
               fontname="Helvetica", labelloc="t", labeljust="c", margin="20,20", rankdir="TB")
        for node in neck_layers:
            node_style = node_style_base.copy()
            node_style["fillcolor"] = type_colors[node["type"]]
            c.node(f"L{node['idx']}", node["label"], **node_style)

    # Head
    with dot.subgraph(name="cluster_head") as c:
        c.attr(label="Head", color="#ffe6e6", style="rounded",
            fontname="Helvetica", labelloc="t", labeljust="c", margin="20,20", rankdir="TB")
        if head_idx >= 0:
            node = layers[head_idx]
            node_style = node_style_base.copy()
            node_style["fillcolor"] = type_colors.get(node.get("type"), "#F7F9FC")

            # --- 让最后一个 head 模块更大 ---
            node_style["width"] = "2.5"       # 横向长度
            # node_style["height"] = "1.2"      # 纵向高度
            # node_style["fontsize"] = "16"     # 字体大一点
            # node_style["fixedsize"] = "true"  # 固定大小，不随文字长度改变

            c.node(f"L{node['idx']}", node["label"], **node_style)

    # --- edges ---
    existing_nodes = {f"L{n['idx']}" for n in layers}
    edge_set = set()
    for src_idx, dst_idx in edges:
        src_id = f"L{src_idx}" if src_idx >= 0 else "Input"
        dst_id = f"L{dst_idx}"
        if src_id not in existing_nodes and src_id != "Input":
            src_id = "Input"
        key = (src_id, dst_id)
        if key not in edge_set:
            edge_set.add(key)
            dot.edge(src_id, dst_id, arrowhead="vee", penwidth="1.1")

    # --- export ---
    out_dir = os.path.dirname(out_file)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    dot.render(out_file, cleanup=True)
    print(f"✅ Saved color-coded graph to {out_file}.{fmt}")


# ---------------- main ----------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python yml2modelgraph.py model.yaml [out_name] [--format svg|png]")
        return
    yml_path = sys.argv[1]
    out_name = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "model_graph"
    fmt = "svg"
    if "--format" in sys.argv:
        try:
            fmt = sys.argv[sys.argv.index("--format") + 1]
        except Exception:
            fmt = "svg"

    with open(yml_path, "r") as f:
        d = yaml.safe_load(f)

    layers, edges, backbone_len = parse_yaml_model(d, input_channels=3)
    draw_graph(layers, edges, backbone_len, out_file=out_name, fmt=fmt)


if __name__ == "__main__":
    main()
