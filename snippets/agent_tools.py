# 摘自 app/graph/nodes.py 第 333-340 行、第 357-373 行
# 仅用于面试核验，不是完整文件

async def agent_tools(state) -> dict:
    """ReAct 行动步(ch08):一切工具经统一执行引擎。"""
    last = state["messages"][-1]
    cid = state.get("conversation_id", 0)
    uid = state.get("user_id", "")
    specs = {s.name: s for s in await registry.get_all_specs()}
    ticket_calls = [tc for tc in last.tool_calls if tc["name"] == "create_ticket"]

    for tc in last.tool_calls:
        if tc["name"] == "submit_refund":
            # submit_refund 在这里就被拦成前端表单、不进执行引擎
            if not business.owns_order(uid, str(tc["args"].get("order_id") or "")):
                not_owned = True
                tool_msgs.append(ToolMessage(
                    content="没有找到这位用户的这笔订单,本次不发起退款。请如实告知没查到,"
                            "并让用户从下面列出的订单里选一笔,不要再调用任何工具。",
                    tool_call_id=tc["id"], name="submit_refund", status="error"))
                continue
            actions.append({"type": "refund_form",
                            "draft": {"order_id": tc["args"].get("order_id", ""),
                                      "reason": tc["args"].get("reason")}})
            tool_msgs.append(ToolMessage(
                content="已把『提交退款工单』选项交给用户确认。请用一句话说明这一单可以退款并停止,不要再调用任何工具。",
                tool_call_id=tc["id"], name="submit_refund"))
