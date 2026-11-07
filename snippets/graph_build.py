# 摘自 app/graph/build.py 第 25-42 行
# 仅用于面试核验，不是完整文件

    b.add_edge(START, "resolve_reference")
    b.add_edge("resolve_reference", "classify_intent")
    b.add_conditional_edges("classify_intent", route_by_intent, {
        "escalate": "complaint_reply",
        "fallback_script": "script_reply",
        "knowledge": "retrieve_knowledge",
        "refund_flow": "fetch_order",
        "business": "main_agent",
    })
    # 退款子流程确定性链:取单 → 检索政策 → 交主力 Agent 判能不能退
    b.add_edge("fetch_order", "retrieve_policy")
    b.add_edge("retrieve_policy", "main_agent")
    # 知识路:检索 → 生成前证据闸
    b.add_edge("retrieve_knowledge", "confidence_check")
    b.add_conditional_edges("confidence_check", confidence_gate, {
        "strong": "main_agent",
        "weak": "fallback_reply",
    })
    # 主力 Agent ReAct 环
    b.add_conditional_edges("main_agent", should_continue, {
        "continue": "agent_tools",
        "stop": "log",
    })
    b.add_edge("agent_tools", "main_agent")
