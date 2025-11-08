# YAML2ModelGraph  

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)  

---

## 项目简介

**YAML2ModelGraph** 是一个将 Ultralytics 模型的 YAML 配置文件，自动生成模型结构图的工具。  

它的特点包括：  

- 支持 **backbone、neck 与 head 层**的分组展示  
- 自动解析各模块 **输入输出通道**  
- 支持 **Concat 输出通道自动计算**  
- 支持 **竖版布局**，**直角边**，便于论文和文档展示  
- **美化节点和子图**，直观展示模型结构  
- 可扩展，可适配 **自定义模块**  

---

## 功能特点

1. **YAML 自动解析**  
   读取模型 YAML 文件，自动解析每一层的模块类型、重复次数、输入输出通道及参数。  

2. **自动生成 Graphviz 图**  
   - Backbone、Neck 和 Head 自动分组  
   - 支持竖版 Top→Bottom 展示  
   - 线条直角连接，整洁美观  
   - 支持输出 SVG 或 PNG 格式  

3. **模块兼容**  
   支持所有常见模块。  

---

## 效果
<details>
<summary>点击展开查看效果图</summary>

<div align="center">
<img src="./yolov8_model_graph.svg" alt="banner" width="500">
</div>

</details>

---

## 安装

### 系统依赖

- Graphviz：用于渲染图形  

  ```bash
  sudo apt install graphviz -y   # Ubuntu/Debian
  sudo apt install graphviz       
  
  brew install graphviz           # macOS
  ```

### Python 依赖

```bash
pip install pyyaml graphviz
```

---

## 使用方法

### 命令行调用

```bash
python yml2modelgraph.py path/to/model.yaml [out_name] [--format svg|png]
```

- `path/to/model.yaml`：模型 YAML 文件路径  
- `[out_name]`：输出文件名（默认 `model_graph_fixed`）  
- `[--format svg|png]`：输出格式（默认 `svg`）  

### 示例

```bash
python yml2modelgraph.py yolov8s.yaml yolov8s_graph --format svg
```

将生成文件 `yolov8s_graph.svg`，包含 Backbone 和 Head 层的详细结构及每层输入输出通道。

---

## 输出示例

每个节点显示信息包括：

- 模块类型  
- 输入通道 → 输出通道  
- 重复次数 n  
- 模块参数 args  

示例节点：

```
Conv
64 → 128
n=1
[3, 3, 2]
```

Edges 使用直角线显示，保证图像整洁美观。Backbone 和 Head 分组显示，便于理解模型结构。

---

## 项目结构

```
YAML2ModelGraph/
├── yml2modelgraph.py    # 核心脚本
├── README.md                         # 项目说明
├── LICENSE                           # MIT License
└── examples/                         # 示例 YAML 文件
```

---

## 开发与贡献

欢迎贡献：

- 增加 HTML 或交互式导出  
- 优化图形美化与排版  

Fork 本项目，提交 Pull Request 即可。

---

## 许可证

本项目使用 **MIT License** 开源，允许商用、修改和分发。  

