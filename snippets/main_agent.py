# 摘自 app/graph/nodes.py 第 311-316 行
# 仅用于面试核验，不是完整文件

async def main_agent(state, config=None) -> dict:
    """ReAct 推理步:调模型(带工具),累加 steps 与 token 消耗。"""
    specs = await registry.get_all_specs()   # ch08 现问现拿:内置+MCP 合并清单,每轮现拉
    model = get_chat_model(streaming=True).bind_tools([s.tool for s in specs])
    msgs = _agent_messages(state)
    _log_model_context(state, msgs)   # ch07:摘要+滑窗进日志,验收 tail -f 可见
    ai: AIMessage = await model.ainvoke(msgs, config)
