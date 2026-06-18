#!/usr/bin/env python3
"""
YOLO Graph Generator v2.0
Usage:
    python main.py model.yaml [output.svg] [--theme NAME] [--head single|multi]
"""

import sys
import themes
import yolo_graph

# ================= 🔧 信息显示配置 =================
# 将这里的 True/False 改为你想要的状态
DISPLAY_CONFIG = {
    "show_channels": True,  # 显示通道 (如 64->128 或 128c)
    "show_repeats":  True,  # 显示堆叠数 (如 n=3)
    "show_stride":   True,  # 显示倍率 (如 /32x)
    "show_args":     False, # 显示详细参数 (如 a:3,2) -> ⚠️ 如果字太多溢出，请关掉这个
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py model.yaml [output.svg] [--theme NAME] [--head single|multi]")
        return

    yaml_path = sys.argv[1]

    out_name = "yolo_graph.svg"
    if len(sys.argv) > 2 and not sys.argv[2].startswith("--"):
        out_name = sys.argv[2]
        if not out_name.endswith(".svg"): out_name += ".svg"

    theme_name = "paper"
    if "--theme" in sys.argv:
        try:
            idx = sys.argv.index("--theme")
            theme_name = sys.argv[idx + 1]
        except IndexError: pass

    head_mode = "single"
    if "--head" in sys.argv:
        try:
            idx = sys.argv.index("--head")
            head_mode = sys.argv[idx + 1]
        except IndexError: pass

    config = themes.get_config(theme_name)

    print(f"🎨 Theme: '{theme_name}' | 🧩 Head: {head_mode} | 📊 Info: {DISPLAY_CONFIG}")
    try:
        yolo_graph.parse_and_layout(yaml_path, out_name, config, DISPLAY_CONFIG, head_mode)
        print(f"✅ Saved to {out_name}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()