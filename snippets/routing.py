# 摘自 app/graph/routing.py 第 7-43 行
# 仅用于面试核验，不是完整文件

INTENT_TO_ROUTE: dict[str, str] = {
    "投诉": "escalate",
    "闲聊": "fallback_script",
    "其他": "fallback_script",
    "商品咨询": "knowledge",
    "退款退货": "refund_flow",
    "售后": "refund_flow",
    "人工": "business",   # ch08:明确要求建工单/转人工 → 主力 Agent 走 create_ticket 确认流
    "物流": "business",
    "订单": "business",
}


def route_by_intent(state) -> str:
    """按意图分流;未知意图保守归 business(让 Agent 自己应对)。"""
    return INTENT_TO_ROUTE.get(state.get("intent", ""), "business")


def confidence_gate(state) -> str:
    """知识路生成前证据闸:强放行、弱兜底。"""
    return "strong" if state.get("evidence_strong") else "weak"


def should_continue(state) -> str:
    """ReAct 停止条件:无 tool_calls 就收敛,步数封顶则强停,否则继续。"""
    last = state["messages"][-1]
    has_tool_calls = isinstance(last, AIMessage) and bool(last.tool_calls)
    if not has_tool_calls:
        return "stop"
    if state.get("steps", 0) >= settings.max_agent_steps:
        return "stop"
    return "continue"
