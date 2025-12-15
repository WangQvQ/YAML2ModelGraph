# YAML2ModelGraph

<div align="right">

[English](README_EN.md) | [中文](README.md)

</div>

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 📖 项目简介

**YAML2ModelGrap** 是一个专业的 YOLO 模型架构可视化工具，能够将 Ultralytics YOLO 模型的 YAML 配置文件自动转换为精美的 SVG 架构图。

### ✨ 核心特性

- 🎨 **9 种精美主题**：从科研论文风到现代糖果色，满足不同场景需求
- 📐 **智能布局**：自动识别 Backbone、Neck、Head 三大模块，智能多列折叠
- 🔗 **清晰连线**：支持多种连线样式（直线、贝塞尔曲线、曼哈顿路由）
- 📊 **信息丰富**：显示模块类型、步长（stride）、通道数等关键信息
- 🎯 **即开即用**：无需额外依赖，纯 Python + SVG 输出

---

## 🖼️ 主题展示

<div align="center">

### 9 种主题风格一览

<table>
<tr>
<td align="center"><b>Paper</b><br/>科研标准风</td>
<td align="center"><b>Candy</b><br/>现代糖果风</td>
<td align="center"><b>Dark</b><br/>暗黑极客风</td>
</tr>
<tr>
<td><img src="svg/graph_paper.svg" width="300"/></td>
<td><img src="svg/graph_candy.svg" width="300"/></td>
<td><img src="svg/graph_dark.svg" width="300"/></td>
</tr>
<tr>
<td align="center"><b>Ocean</b><br/>科技海洋风</td>
<td align="center"><b>Retro</b><br/>复古暖阳风</td>
<td align="center"><b>Blueprint</b><br/>工程蓝图风</td>
</tr>
<tr>
<td><img src="svg/graph_ocean.svg" width="300"/></td>
<td><img src="svg/graph_retro.svg" width="300"/></td>
<td><img src="svg/graph_blueprint.svg" width="300"/></td>
</tr>
<tr>
<td align="center"><b>Forest</b><br/>森林氧吧风</td>
<td align="center"><b>Paper RYB</b><br/>学术三原色 ⭐</td>
<td align="center"><b>Journal</b><br/>现代期刊风</td>
</tr>
<tr>
<td><img src="svg/graph_forest.svg" width="300"/></td>
<td><img src="svg/graph_paper_ryb.svg" width="300"/></td>
<td><img src="svg/graph_journal.svg" width="300"/></td>
</tr>
</table>

> 💡 **提示**：所有主题的完整 SVG 文件位于 `svg/` 目录，可直接查看或用于论文/文档

</div>

---

## 🚀 快速开始

### 安装依赖

```bash
pip install pyyaml
```

### 基本使用

```bash
python main.py examples/yolov8.yaml output.svg --theme paper
```

**参数说明：**
- `examples/yolov8.yaml`：输入的 YAML 模型配置文件
- `output.svg`：输出的 SVG 文件路径（可选，默认为 `yolo_graph.svg`）
- `--theme paper`：选择主题风格（可选，默认为 `paper`）

---

## 🎨 主题风格

v1.0 版本提供 **9 种精心设计的主题**，适用于不同场景：

### 1. 科研标准风 (Paper) - 默认主题

**特点：** 黑白灰配色、Times New Roman 字体、极简线条  
**场景：** 专为 IEEE / CVPR / 毕业论文插图设计，打印效果最好


```bash
python main.py examples/yolov8.yaml svg/graph_paper.svg --theme paper
```
### 2. 现代糖果风 (Candy)

**特点：** 莫兰迪色系（淡蓝/淡橙）、大圆角、无衬线字体  
**场景：** 适合 PPT 演示、技术博客、海报，视觉效果活泼现代

```bash
python main.py examples/yolov8.yaml svg/graph_candy.svg --theme candy
```

### 3. 暗黑极客风 (Dark)

**特点：** 深色背景、高对比度线条、代码风格字体  
**场景：** 适合深色模式阅读、屏幕演示、体现"硬核"技术感

```bash
python main.py examples/yolov8.yaml svg/graph_dark.svg --theme dark
```

### 4. 科技海洋风 (Ocean)

**特点：** 不同深浅的蓝色调、清爽专业  
**场景：** 适合商务汇报、科技公司技术白皮书

```bash
python main.py examples/yolov8.yaml svg/graph_ocean.svg --theme ocean
```

### 5. 复古暖阳风 (Retro)

**特点：** 暖米色背景（Gruvbox 风格）、打字机字体  
**场景：** 适合长时间阅读（护眼）、追求复古文艺感的文档

```bash
python main.py examples/yolov8.yaml svg/graph_retro.svg --theme retro
```

### 6. 工程蓝图风 (Blueprint)

**特点：** 深蓝底色、白色细线条、CAD 工程字体  
**场景：** 体现"架构设计"、"底层逻辑"的硬核工程图

```bash
python main.py examples/yolov8.yaml svg/graph_blueprint.svg --theme blueprint
```

### 7. 森林氧吧风 (Forest)

**特点：** 绿色系配色、清新自然  
**场景：** 护眼风格，或用于强调环保/轻量化的主题

```bash
python main.py examples/yolov8.yaml svg/graph_forest.svg --theme forest
```

### 8. 学术三原色风 (Paper RYB) ⭐ 推荐

**特点：** 经典红黄蓝配色、极度降低饱和度，模块区分清晰  
**场景：** 适合需要清晰区分 Backbone/Neck/Head 三大模块结构的论文插图

```bash
python main.py examples/yolov8.yaml svg/graph_paper_ryb.svg --theme paper_ryb
```

### 9. 现代期刊风 (Journal)

**特点：** 极简冷淡风、背景几乎隐形，最严谨的学术风格  
**场景：** 适合 Springer 或 Nature 子刊的图表风格

```bash
python main.py examples/yolov8.yaml svg/graph_journal.svg --theme journal
```

---

## 📋 功能详解

### 自动模块识别

工具会自动识别 YAML 配置中的模块类型，包括：
- **Backbone 模块**：Conv、C2f、SPPF 等
- **Neck 模块**：Upsample、Concat、C2f 等
- **Head 模块**：Detect 等

### 智能布局算法

- **Backbone**：单列垂直布局，清晰展示特征提取流程
- **Neck**：智能多列折叠，当模块过多时自动分列显示
- **Head**：根据输入源自动对齐，保持视觉连贯性

### 连线样式

- **垂直直连**：同列相邻模块使用直线连接
- **贝塞尔曲线**：跨列连接使用平滑曲线
- **曼哈顿路由**：Backbone 到 Neck 使用直角路由
- **虚线标识**：跨模块或长距离连接使用虚线

### 信息展示

每个节点显示：
- **主标签**：模块类型（如 Conv、C2f、Detect）
- **副标签**：步长和通道数（如 `8x / 256c`）

#### 信息显示配置

在 `main.py` 中可以通过 `DISPLAY_CONFIG` 字典自定义节点上显示的信息：

```python
DISPLAY_CONFIG = {
    "show_channels": True,  # 显示通道 (如 64->128 或 128c)
    "show_repeats":  True,  # 显示堆叠数 (如 n=3)
    "show_stride":   True,  # 显示倍率 (如 /32x)
    "show_args":     False, # 显示详细参数 (如 a:3,2) -> ⚠️ 如果字太多溢出，请关掉这个
}
```

**配置项说明：**
- `show_channels`：是否显示通道数变化（如 `64->128` 或 `128c`）
- `show_repeats`：是否显示模块堆叠次数（如 `n=3` 表示重复 3 次）
- `show_stride`：是否显示步长倍率（如 `/32x` 表示下采样 32 倍）
- `show_args`：是否显示详细参数（如 `a:3,2`），**注意**：如果节点信息过多导致文字溢出，建议将此选项设为 `False`

---

## 📁 项目结构

```
YAML2ModelGraph/
├── main.py              # 主程序入口
├── yolo_graph.py        # 核心解析和布局逻辑
├── themes.py            # 主题配置定义
├── README.md            # 项目文档
├── examples/            # 示例 YAML 文件
│   ├── yolov8.yaml
│   ├── yolo11.yaml
│   ├── yolo12.yaml
│   └── yolov9s.yaml
└── svg/                 # 生成的 SVG 示例
    ├── graph_paper.svg
    ├── graph_candy.svg
    ├── graph_dark.svg
    ├── graph_ocean.svg
    ├── graph_retro.svg
    ├── graph_blueprint.svg
    ├── graph_forest.svg
    ├── graph_paper_ryb.svg
    └── graph_journal.svg
```

---

## 🔧 高级用法

### 自定义主题

编辑 `themes.py` 文件，可以：
- 修改现有主题的颜色、字体、圆角等参数
- 添加新的主题配置
- 调整布局参数（节点大小、间距等）

### 自定义信息显示

编辑 `main.py` 中的 `DISPLAY_CONFIG` 字典，可以控制节点上显示哪些信息：

```python
DISPLAY_CONFIG = {
    "show_channels": True,  # 显示通道数
    "show_repeats":  True,  # 显示堆叠数
    "show_stride":   True,  # 显示步长倍率
    "show_args":     False, # 显示详细参数（建议关闭以避免文字溢出）
}
```

**使用建议：**
- 如果生成的图表中节点文字过多导致溢出，可以将 `show_args` 设为 `False`
- 对于简单的模型可视化，可以关闭部分选项以获得更简洁的图表
- 对于详细的架构分析，可以全部开启以获得完整信息

### 支持的 YAML 格式

工具兼容 Ultralytics YOLO 系列的 YAML 格式：

```yaml
backbone:
  - [-1, 1, Conv, [64, 3, 2]]
  - [-1, 3, C2f, [128, True]]
  # ...

head:
  - [-1, 1, nn.Upsample, [None, 2, "nearest"]]
  - [[-1, 6], 1, Concat, [1]]
  # ...
```

---

## 📸 效果预览

所有主题的示例图已保存在 `svg/` 目录下，您可以直接查看不同主题的视觉效果。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**可能的改进方向：**
- 添加更多主题风格
- 支持自定义节点样式
- 优化复杂模型的布局算法
- 添加交互式 SVG 功能

---

## 📄 许可证

本项目使用 **MIT License** 开源，允许商用、修改和分发。

---

## 🙏 致谢

感谢 Ultralytics 团队提供的 YOLO 框架和模型定义格式。

---

**版本：** v1.0  