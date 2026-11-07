# MewHelp 脱敏证据包

本仓库用于面试核验，只保留可公开或可脱敏的关键代码摘录、评估报告和说明文档，不包含完整业务仓库、`.env`、运行日志、会话检查点和模型产物。

## 项目一句话

MewHelp / 喵喵优选是一个电商智能客服 Agent：用户提问后，系统先做指代消解和九类意图识别，再分流到知识咨询、退款、业务工具、投诉、闲聊五条路；知识路用 Milvus 混合检索 + 重排 + 证据闸，业务路用 ReAct 调订单、物流、售后 MCP 工具。

## 三个必须说明的边界

1. **项目基线来自课程配套源码 MewHelp**，README 中有明确说明。本证据包只陈述代码事实，不把课程基线说成个人从零原创。
2. **业务数据是 mock**。订单、商品、物流、保修、退货进度都由确定性 mock 函数生成，不接真实订单/物流系统。
3. **知识库是平台规则，不是法律法条库**。没有《电子商务法》《消费者权益保护法》的法条匹配，也没有法律意见审核；它做的是平台规则问答和业务风控。

## 证据索引

| 结论 | 证据摘录 | 原始位置 |
|---|---|---|
| LangGraph 图编排、五路分流、证据闸、ReAct 环 | [graph_build.py](snippets/graph_build.py#L1-L26) | `app/graph/build.py` 第 25-42 行 |
| 九类意图到五出口的映射 | [routing.py](snippets/routing.py#L1-L11) | `app/graph/routing.py` 第 7-17 行 |
| 知识路强/弱证据条件边 | [routing.py](snippets/routing.py#L1-L28) | `app/graph/routing.py` 第 25-27 行 |
| ReAct 停止条件与步数封顶 | [routing.py](snippets/routing.py#L1-L28) | `app/graph/routing.py` 第 30-43 行 |
| 主力 Agent 绑定内置 + MCP 工具 | [main_agent.py](snippets/main_agent.py#L1-L9) | `app/graph/nodes.py` 第 311-316 行 |
| 工具行动节点、退款入口拦截 | [agent_tools.py](snippets/agent_tools.py#L1-L25) | `app/graph/nodes.py` 第 333-340、357-373 行 |
| 统一执行引擎、写操作权限门、身份注入 | [tool_engine.py](snippets/tool_engine.py#L1-L22) | `app/tools/engine.py` 第 115-121、159-174 行 |
| 写工具清单与 ToolSpec | [registry.py](snippets/registry.py#L1-L18) | `app/tools/registry.py` 第 13-31 行 |
| 物流 MCP 工具真实实现 | [mcp_logistics.py](snippets/mcp_logistics.py#L1-L20) | `mcp_servers/logistics_server.py` 第 21-38 行 |
| MCP 返回结果翻译与字段裁剪 | [mcp_client.py](snippets/mcp_client.py#L1-L9) | `app/tools/mcp_client.py` 第 20-24、41-42 行 |
| 订单查询与归属校验 | [query_order.py](snippets/query_order.py#L1-L16) | `app/tools/builtin/orders.py` 第 10-25、42-43 行 |
| 300 题四策略评估常量 | [eval_ch04.py](snippets/eval_ch04.py#L1-L11) | `scripts/eval_ch04.py` 第 44-54 行 |
| 兜底问题来源标签修正的测试断言 | [confidence_gate_test.py](snippets/confidence_gate_test.py#L1-L20) | `tests/graph/test_ch09_confidence_gate.py` 第 40-59 行 |

## 关键指标

评估集 300 题，5 个桶各 60 题：政策、型号、口语、跨文档、库里无答案。

| 指标 | 值 | 口径 |
|---|---|---|
| Recall@5 | **0.983** | `hybrid_rerank` 总体，四舍五入 98% |
| MRR | **0.894** | 四个可作答桶宏平均 |
| D 桶拒答率 | **1.000（60/60）** | 库里无答案，应拒答 |
| Faithfulness | A 0.983；B/C/E 1.000 | 裁判模型比对答案与本轮 10 条证据 |
| 编造个案 | **1 例 / 300 = 0.33%** | 本轮判出率，个案 A30 |
| 人工确认率 | **0 / 300 = 0%** | 人工确认已解决 |
| 该拒没拒 | **0 例** | D 桶误答 |

报告 metadata：`n_samples=300`、`kb_chunks=51`、`recall_k=5`、`retrieve_k=10`、`chat_model=MiniMax-M2.5`、生成时间 `2026-08-07 20:38`。

**口径说明：** 简历或口头材料若写“幻觉率 0.7%”，与当前报告不一致；当前报告判出率为 **0.33%**，人工确认率为 **0%**。

报告文件：

- [rag_eval.json](reports/rag_eval.json)
- [rag_eval.txt](reports/rag_eval.txt)
- [confidence_calibration.txt](reports/confidence_calibration.txt)
- [confidence_calibration.json](reports/confidence_calibration.json)

评估集：

- [eval_ch04_redacted.jsonl](data/eval_ch04_redacted.jsonl)

该评估集已扫描手机号、邮箱、长订单号等模式，未发现命中；仍建议人工抽查后再公开。

## 一条真实工具调用

用户问题：`我的订单 1001 到哪了？`

第一步，`query_order`：

```json
{"order_id": "1001"}
```

原始返回：

```json
{
  "order_id": "1001",
  "status": "已付款",
  "amount": 1739,
  "created_at": "2026-07-04 10:00",
  "product": "智能猫砂盆",
  "tracking_no": "SF213502378238"
}
```

第二步，`query_logistics`：

```json
{"tracking_no": "SF213502378238"}
```

MCP Server 原始返回：

```json
{
  "tracking_no": "SF213502378238",
  "status_code": "PICKED_UP",
  "current_city": "成都",
  "trace": ["成都分拨中心 已发出", "内部状态码:PICKED_UP"],
  "carrier_code": "SF-EXP-01"
}
```

客户端格式化后回填给模型：

```json
{
  "tracking_no": "SF213502378238",
  "status": "已揽件",
  "current_city": "成都",
  "trace": ["成都分拨中心 已发出", "内部状态码:PICKED_UP"]
}
```

`status_code` 被翻译为“已揽件”，`carrier_code` 被剔除；证据见 [mcp_client.py](snippets/mcp_client.py#L1-L10)。

最终答复示例：

> 您的订单 1001 是智能猫砂盆，状态为已付款，金额 1739 元，下单时间 2026-07-04 10:00。物流单号 SF213502378238，目前已在成都揽件，最新轨迹为“成都分拨中心已发出”。

每次工具调用写入 `tool_audit_logs`，记录工具名、参数、结果摘要、状态、重试次数和耗时。

## 一次真实误判与修正

**现象：** 早期所有兜底问题落库时 `source` 都是 `retrieval_low_conf`，分不清“检索置信度低”和“检索过了但模型自检说证据不足”。

**定位：** `fallback_reply` 写库来源是固定值；`confidence_check` 没有把 `fallback_source` 传下去。

**修正：** 置信度低写 `retrieval_low_conf`，自检不通过写 `self_check`；`fallback_reply` 读取 `state["fallback_source"]`；旧路径缺字段时回落 `retrieval_low_conf`。

**验证：** [confidence_gate_test.py](snippets/confidence_gate_test.py#L1-L20) 分别断言两种来源；`tests/db/test_low_confidence.py` 再断言 `source` 正确落库。

**未关闭个案：** A30 把“纸质专票快递费到付”外推成“电子发票快递费由平台承担”。它仍在“未解决”台账里，没有被说成已修复。

## 目录结构

```text
mewhelp-evidence/
├─ README.md
├─ snippets/
│  ├─ graph_build.py
│  ├─ routing.py
│  ├─ main_agent.py
│  ├─ agent_tools.py
│  ├─ tool_engine.py
│  ├─ registry.py
│  ├─ mcp_logistics.py
│  ├─ mcp_client.py
│  ├─ query_order.py
│  ├─ eval_ch04.py
│  └─ confidence_gate_test.py
├─ reports/
│  ├─ rag_eval.json
│  ├─ rag_eval.txt
│  ├─ confidence_calibration.json
│  └─ confidence_calibration.txt
├─ data/
│  └─ eval_ch04_redacted.jsonl
└─ screenshots/
   └─ README.md
```

## 脱敏说明

本包不包含：

- `.env`、`.env.local` 等真实密钥文件；
- `.venv/`、`__pycache__/`、`.pytest_cache/`；
- `log/`、`data/*.log`、`*.pid`；
- `data/ch05_checkpoints.sqlite`、`*.db`；
- `data/ch10/` 模型产物；
- `.idea/` 本地配置；
- 真实手机号、姓名、订单号、API Key。

只保留：

- 关键代码摘录；
- 脱敏评估集；
- 评估报告；
- 说明文档；
- 截图目录说明（实际截图需本人补拍并打码）。

## 已知限制

- 业务数据是 mock，不代表真实生产订单/物流；
- 知识库是平台规则，不是法律法条库；
- 没有法条版本、生效日期、法律意见审核；
- 报告生成模型是 `MiniMax-M2.5`，不是当前运行环境的 `deepseek-chat`；
