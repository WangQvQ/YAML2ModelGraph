"""
yolo_graph.py - Core logic for parsing YAML and generating SVG
"""
import yaml
import math

class SVGBuilder:
    def __init__(self, config):
        self.config = config
        self.elements = []
        self.width = 0
        self.height = 0

    def get_defs(self):
        grads = self.config["gradients"]
        return f'''
        <defs>
            <filter id="shadow" x="-20%" y="-20%" width="150%" height="150%">
                <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
                <feOffset dx="2" dy="2" result="offsetblur"/>
                <feComponentTransfer><feFuncA type="linear" slope="0.15"/></feComponentTransfer>
                <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
            
            <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto" markerUnits="strokeWidth">
                <path d="M0,0 L0,6 L6,3 z" fill="{self.config["colors"]["line"]}" />
            </marker>
            
            <linearGradient id="grad_bb" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{grads["grad_bb_start"]};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{grads["grad_bb_end"]};stop-opacity:1" />
            </linearGradient>
            <linearGradient id="grad_neck" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{grads["grad_neck_start"]};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{grads["grad_neck_end"]};stop-opacity:1" />
            </linearGradient>
            <linearGradient id="grad_head" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{grads["grad_head_start"]};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{grads["grad_head_end"]};stop-opacity:1" />
            </linearGradient>
            <linearGradient id="grad_concat" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{grads["grad_concat_start"]};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{grads["grad_concat_end"]};stop-opacity:1" />
            </linearGradient>
            <linearGradient id="grad_node" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{grads["grad_node_start"]};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{grads["grad_node_end"]};stop-opacity:1" />
            </linearGradient>
        </defs>
        '''

    def get_header(self):
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}">
        <style>
            text {{ font-family: "{self.config['font']}"; }}
        </style>
        {self.get_defs()}
        '''

    def add_rect(self, x, y, w, h, fill_id, label, sub, is_concat=False, type_color=None):
        fill_attr = f"url(#{fill_id})"
        filter_attr = 'filter="url(#shadow)"'
        stroke_w = "1.5" if is_concat else "1.0"
        
        # 1. 主体矩形
        self.elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{self.config["radius"]}" fill="{fill_attr}" stroke="{self.config["colors"]["stroke"]}" stroke-width="{stroke_w}" {filter_attr}/>')
        
        # 2. 色条 (Type Strip) - 4px 宽
        if type_color:
            strip_w = 5
            # 使用 clipPath 确保色条贴合左侧圆角
            clip_id = f"clip_{int(x)}_{int(y)}"
            self.elements.append(f'<clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{self.config["radius"]}" /></clipPath>')
            
            # 绘制色条，使用 clipPath 裁切多余部分
            self.elements.append(f'<rect x="{x}" y="{y}" width="{strip_w}" height="{h}" fill="{type_color}" clip-path="url(#{clip_id})" />')

        cx, cy = x + w/2, y + h/2
        # 文字稍微右移避开色条
        text_offset = 2
        
        self.elements.append(f'<text x="{cx+text_offset}" y="{cy-8}" font-weight="bold" font-size="14" fill="{self.config["colors"]["text_main"]}" text-anchor="middle" dominant-baseline="middle">{label}</text>')
        self.elements.append(f'<text x="{cx+text_offset}" y="{cy+11}" font-size="10" fill="{self.config["colors"]["text_sub"]}" text-anchor="middle" dominant-baseline="middle">{sub}</text>')
        return {"L": (x, cy), "R": (x+w, cy), "T": (cx, y), "B": (cx, y+h), "rect": (x, y, w, h)}

    def add_bg_lane(self, x, w, h, label, color):
        self.elements.insert(0, f'<rect x="{x}" y="30" width="{w}" height="{h-30}" fill="{color}" />')
        self.elements.append(f'<text x="{x+w/2}" y="55" font-weight="bold" font-size="18" fill="{self.config["colors"]["text_main"]}" text-anchor="middle" letter-spacing="1">{label}</text>')
        self.elements.append(f'<line x1="{x+20}" y1="65" x2="{x+w-20}" y2="65" stroke="#90A4AE" stroke-width="1"/>')

    def add_link(self, p1, p2, dashed=False, routing_type="standard"):
        x1, y1 = p1; x2, y2 = p2
        path = ""
        
        if routing_type == "vertical_straight":
            path = f"M {x1} {y1} L {x2} {y2}"
        elif routing_type == "manhattan":
            mid_x = (x1 + x2) / 2
            path = f"M {x1} {y1} C {mid_x} {y1}, {mid_x} {y2}, {x2} {y2}"
        elif routing_type == "detour_right":
            offset = 60
            cp1_x = x1 + offset; cp1_y = y1
            cp2_x = x2 + offset; cp2_y = y2
            path = f"M {x1} {y1} C {cp1_x} {cp1_y}, {cp2_x} {cp2_y}, {x2} {y2}"
        else:
            dist_x = abs(x2 - x1)
            cp1_x = x1 + dist_x * 0.5; cp1_y = y1
            cp2_x = x2 - dist_x * 0.5; cp2_y = y2
            path = f"M {x1} {y1} C {cp1_x} {cp1_y}, {cp2_x} {cp2_y}, {x2} {y2}"

        dash_attr = 'stroke-dasharray="5,3"' if dashed else ''
        self.elements.append(f'<path d="{path}" stroke="{self.config["colors"]["line"]}" stroke-width="1.2" fill="none" {dash_attr} marker-end="url(#arrow)" />')

    def generate(self):
        return self.get_header() + "\n".join(self.elements) + "</svg>"


def parse_and_layout(yaml_path, out_file, config, display_config, head_mode="single"):
    with open(yaml_path, 'r', encoding='utf-8') as f: d = yaml.safe_load(f)
    full_seq = d.get('backbone', []) + d.get('head', [])
    backbone_len = len(d.get('backbone', []))
    
    layers = []
    # 记录每一层的 output_channels，用于 Concat 回溯
    # 格式: idx -> channels
    layer_channels = {}
    
    # 初始通道
    ch = [3]
    curr_stride = 1
    
    for i, item in enumerate(full_seq):
        f_idx, n, m, args = item
        args = args or []
        m_str = str(m)
        from_idxs = [f_idx] if isinstance(f_idx, int) else list(f_idx)
        abs_from = [(src if src >= 0 else i + src) for src in from_idxs]
        
        c1 = ch[-1]
        
        label = m_str.replace("nn.modules.", "").replace("ularytics.", "").replace("C2f", "C2f")
        if 'Conv' in label: label = "Conv"
        
        # --- 修复 Concat 通道数 ---
        if 'Concat' in label:
            # Concat 的输出通道数 = 所有输入源的通道数之和
            c2 = 0
            for src_idx in abs_from:
                # 尝试从已记录的 layers 中获取
                if src_idx in layer_channels:
                    c2 += layer_channels[src_idx]
                else:
                    # 如果找不到（比如来自 Input），假设 c1 (不太可能)
                    c2 += c1 
        else:
            # 普通模块 (Conv, C2f等)，输出通道通常在 args[0]
            c2 = args[0] if (args and isinstance(args[0], int)) else c1
            
        # 记录当前层的输出通道，供后续 Concat 使用
        layer_channels[i] = c2
        
        next_stride = curr_stride
        if 'Conv' in m_str:
            for a in args: 
                if a == 2: next_stride *= 2; break
        elif 'Upsample' in m_str: next_stride /= 2
        
        # 泳道分配
        col = 0
        if i >= backbone_len:
            if 'Detect' in m_str: col = 2
            else: col = 1

        # --- 颜色与渐变逻辑 ---
        fill_id = "grad_node"
        if col == 0: fill_id = "grad_bb"
        elif col == 1: fill_id = "grad_neck"
        elif col == 2: fill_id = "grad_head"
        
        is_concat = False
        if 'Concat' in label: 
            fill_id = "grad_concat"; is_concat = True
            
        # --- 核心：匹配色条颜色 ---
        type_color = config["type_colors"].get("Other") # 默认灰
        if "Conv" in label: type_color = config["type_colors"]["Conv"]
        elif "Concat" in label: type_color = config["type_colors"]["Concat"]
        elif "Detect" in label: type_color = config["type_colors"]["Detect"]
        elif "Upsample" in label: type_color = config["type_colors"]["Upsample"]
        elif "C2f" in label: type_color = config["type_colors"]["C2f"]
        
        # --- 信息构建 ---
        info_parts = []
        if display_config.get("show_channels", True):
            if c1 != c2 and "Detect" not in label:
                info_parts.append(f"{c1}→{c2}")
            else:
                info_parts.append(f"{c2}c")
        
        if display_config.get("show_repeats", True) and n > 1:
            info_parts.append(f"n={n}")
            
        if display_config.get("show_args", False) and args:
            # Concat 的参数通常是维度轴，没必要显示
            if 'Concat' not in label:
                rem_args = args[1:] if (args and isinstance(args[0], int)) else args
                if rem_args:
                    args_str = str(rem_args).replace(" ", "")
                    if len(args_str) > 10: args_str = args_str[:8] + ".."
                    info_parts.append(f"a:{args_str}")
        
        if display_config.get("show_stride", True):
            info_parts.append(f"/{int(next_stride)}x")
            
        sub_text = " ".join(info_parts)
        if not sub_text: sub_text = "Layer"

        # --- Detect 多头拆分：每个输入源生成一个独立的 Detect 节点 ---
        if 'Detect' in m_str and len(abs_from) > 1 and head_mode == "multi":
            scale_names = ["P3/8", "P4/16", "P5/32", "P6/64"]
            for si, src_idx in enumerate(abs_from):
                scale = scale_names[si] if si < len(scale_names) else f"P{si+3}/?"
                src_stride = layers[src_idx]["stride"] if src_idx < len(layers) else (8 * (2 ** si))
                detect_label = f"Detect ({scale})"
                src_ch = layer_channels.get(src_idx, c1)
                detect_parts = []
                if display_config.get("show_channels", True):
                    detect_parts.append(f"{src_ch}c")
                if display_config.get("show_stride", True):
                    detect_parts.append(f"/{src_stride}x")
                detect_sub = " ".join(detect_parts) if detect_parts else "Head"
                detect_coord_key = f"{i}_d{si}"
                layers.append({
                    "idx": i, "detect_idx": detect_coord_key,
                    "label": detect_label, "sub": detect_sub,
                    "stride": src_stride, "col": 2,
                    "from": [src_idx], "fill_id": "grad_head",
                    "is_concat": False, "type_color": config["type_colors"]["Detect"]
                })
        else:
            layers.append({
                "idx": i, "label": label, "sub": sub_text,
                "stride": int(next_stride), "col": col,
                "from": abs_from, "fill_id": fill_id, "is_concat": is_concat,
                "type_color": type_color
            })
        ch.append(c2)
        curr_stride = next_stride

    # 2. 布局计算 (保持 v20 逻辑)
    svg = SVGBuilder(config)
    coords = {} 
    
    # Backbone
    current_y = 100
    backbone_items = [l for l in layers if l['col'] == 0]
    for l in backbone_items:
        center_x = config["lane_width_bb"] / 2
        props = svg.add_rect(center_x - config["node_w"]/2, current_y, config["node_w"], config["node_h"], l['fill_id'], l['label'], l['sub'], l['is_concat'], l['type_color'])
        props['col'] = 0; props['neck_col_id'] = -1
        coord_key = l.get('detect_idx', l['idx'])
        coords[coord_key] = props
        current_y += config["bb_step"]
    max_bb_y = current_y - config["bb_step"] + config["node_h"]
    
    # Neck
    neck_items = [l for l in layers if l['col'] == 1]
    neck_start_y = 100
    neck_curr_y = neck_start_y
    neck_col_idx = 0 
    neck_cols_layout = [[], [], []]
    
    for l in neck_items:
        if neck_curr_y > max_bb_y and neck_col_idx < 2:
            neck_col_idx += 1; neck_curr_y = neck_start_y
        neck_cols_layout[neck_col_idx].append(l)
        neck_curr_y += config["neck_step"]
        
    actual_neck_width = 0
    for c_id, items in enumerate(neck_cols_layout):
        if not items: continue
        base_x = config["lane_width_bb"] + c_id * (config["lane_width_neck_col"] + config["col_gap"])
        center_x = base_x + config["lane_width_neck_col"] / 2
        curr_y = neck_start_y
        for l in items:
            props = svg.add_rect(center_x - config["node_w"]/2, curr_y, config["node_w"], config["node_h"], l['fill_id'], l['label'], l['sub'], l['is_concat'], l['type_color'])
            props['col'] = 1; props['neck_col_id'] = c_id
            coord_key = l.get('detect_idx', l['idx'])
            coords[coord_key] = props
            curr_y += config["neck_step"]
        actual_neck_width = base_x + config["lane_width_neck_col"]

    # Head
    head_items = [l for l in layers if l['col'] == 2]
    head_start_x = actual_neck_width + config["col_gap"]

    if head_mode == "multi":
        # 多头模式：从最底部往上堆叠，最底下一个和底部模块对齐
        bottom_y = max((v['rect'][1] + v['rect'][3] for v in coords.values()), default=max_bb_y)
        head_y = bottom_y - config["node_h"] - (len(head_items) - 1) * config["neck_step"]
        for l in head_items:
            center_x = head_start_x + config["lane_width_head"] / 2
            coord_key = l.get('detect_idx', l['idx'])
            props = svg.add_rect(center_x - config["node_w"]/2, head_y, config["node_w"], config["node_h"], l['fill_id'], l['label'], l['sub'], l['is_concat'], l['type_color'])
            props['col'] = 2; props['neck_col_id'] = 99
            coords[coord_key] = props
            head_y += config["neck_step"]
    else:
        # 单头模式：Detect 节点居中于输入源的平均 y 坐标
        head_curr_y = neck_start_y
        for l in head_items:
            center_x = head_start_x + config["lane_width_head"] / 2
            coord_key = l.get('detect_idx', l['idx'])
            src_ys = [coords[s]['rect'][1] for s in l['from'] if s in coords]
            target_y = sum(src_ys)/len(src_ys) if src_ys else head_curr_y
            if target_y < head_curr_y: target_y = head_curr_y
            props = svg.add_rect(center_x - config["node_w"]/2, target_y, config["node_w"], config["node_h"], l['fill_id'], l['label'], l['sub'], l['is_concat'], l['type_color'])
            props['col'] = 2; props['neck_col_id'] = 99
            coords[coord_key] = props
            head_curr_y = target_y + config["neck_step"]

    # Routing
    for l in layers:
        coord_key = l.get('detect_idx', l['idx'])
        if coord_key not in coords: continue
        dst = coords[coord_key]
        for src_idx in l['from']:
            if src_idx not in coords: continue
            src = coords[src_idx]
            p1 = src['rect']; p2 = dst['rect']
            start_pt = (p1[0]+p1[2], p1[1]+p1[3]/2); end_pt = (p2[0], p2[1]+p2[3]/2)
            dashed = (l['col'] != src['col']) or abs(l['idx'] - src_idx) > 1
            routing = "standard"
            
            if l['col'] == 0 and src['col'] == 0:
                if abs(l['idx'] - src_idx) == 1:
                    start_pt = (p1[0]+p1[2]/2, p1[1]+p1[3]); end_pt = (p2[0]+p2[2]/2, p2[1])
                    routing = "vertical_straight"; dashed = False
            elif src['col'] == 0 and dst['col'] == 1: routing = "manhattan"
            elif src['col'] == 1 and dst['col'] == 1 and src['neck_col_id'] == dst['neck_col_id']:
                if abs(l['idx'] - src_idx) == 1:
                    start_pt = (p1[0]+p1[2]/2, p1[1]+p1[3]); end_pt = (p2[0]+p2[2]/2, p2[1])
                    routing = "vertical_straight"
                else:
                    start_pt = (p1[0]+p1[2], p1[1]+p1[3]/2); end_pt = (p2[0]+p2[2], p2[1]+p2[3]/2)
                    routing = "detour_right"
            elif dst['rect'][0] < src['rect'][0]:
                start_pt = (p1[0], p1[1]+p1[3]/2); end_pt = (p2[0]+p2[2], p2[1]+p2[3]/2)
            
            svg.add_link(start_pt, end_pt, dashed, routing)

    # 计算所有节点的最大 y 坐标（包括 Head 区域的 Detect 节点）
    max_all_y = max_bb_y
    for v in coords.values():
        node_bottom = v['rect'][1] + v['rect'][3]
        if node_bottom > max_all_y: max_all_y = node_bottom

    # Output
    total_w = head_start_x + config["lane_width_head"]
    svg.width = total_w; svg.height = max_all_y + 50
    svg.add_bg_lane(0, config["lane_width_bb"], svg.height, "Backbone", config["colors"]["bg_backbone"])
    svg.add_bg_lane(config["lane_width_bb"], head_start_x - config["lane_width_bb"], svg.height, "Neck", config["colors"]["bg_neck"])
    svg.add_bg_lane(head_start_x, config["lane_width_head"], svg.height, "Head", config["colors"]["bg_head"])

    with open(out_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(svg.generate())