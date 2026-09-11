# graph-deepresearch-skill

[English](README_EN.md)

图谱化深度研究技能：DAG 编排、并行调研、独立事实核查、对抗审查、全链路来源引用。遵循开放的 [Agent Skills](https://agentskills.io) 规范，Claude Code / Codex / Cursor / ZCode 等 20 余种客户端通用。

## 技能列表

### [graph-deepresearch](SKILL.md) 🔍

把复杂研究课题拆解为独立子问题，派出并行 subagent 调研，再由核查者与对抗审查者独立验证每条结论，输出带来源引用和置信度的结构化报告（Markdown + JSON）。

触发示例：

- "深度研究一下 X"
- "从多个角度调研 Y"
- "帮我核实这个说法是否属实"
- "对比 A 和 B，给我一份带来源的报告"

## 流水线

```
拆解（Plan）→ 并行调研（Worker）→ 核查 + 对抗审查（Verify）→ 综合（Merge）→ 报告（Report）
```

- 每个子问题由独立的 subagent worker 并行调研
- 每条结论同时经过核查者（求证）与对抗审查者（证伪），两者互相隔离
- 决策类课题可选原则库推演：事实 → 多情景预测（乐观 / 基准 / 悲观）
- 每条结论附来源 URL、可信度评级与置信度评分

## 安装

一条命令安装（[skills CLI](https://skills.sh/)）：

```bash
npx skills add yuzhi9257/graph-deepresearch-skill
```

或手动软链到技能目录：

```bash
git clone https://github.com/yuzhi9257/graph-deepresearch-skill.git
ln -s "$(pwd)/graph-deepresearch-skill" ~/.agents/skills/graph-deepresearch
```

## 前置条件

调研 worker 默认使用 Tavily 搜索（有免费额度）：

```bash
curl -fsSL https://cli.tavily.com/install.sh | bash && tvly login
```

Tavily 不可用时自动降级为 web_fetch，再降级为带时效警告的模型知识。

## 输出校验

```bash
python scripts/validate_output.py research_output.json
```

## 目录结构

```
├── SKILL.md
├── references/
│   ├── search-strategies.md
│   ├── verification.md
│   ├── output-formats.md
│   └── pitfalls.md
└── scripts/
    └── validate_output.py
```

## 许可证

[MIT](LICENSE)
