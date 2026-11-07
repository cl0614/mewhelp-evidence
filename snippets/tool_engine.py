# 摘自 app/tools/engine.py 第 115-121 行、第 159-174 行
# 仅用于面试核验，不是完整文件

async def execute_tool_call(
    tool_call: dict, conversation_id: int, specs: dict[str, ToolSpec],
    *, confirmed: bool = False, deny_note: str | None = None, user_id: str = "",
) -> ToolRun:
    """统一入口(never-raises 契约):无论校验拦下、权限拒绝还是真故障,一律回 ToolRun,
    坏消息包成 ToolMessage 回灌模型。confirmed 是写操作确认令牌,只能由 agent_tools 在
    interrupt 确认后传入——模型自己无法绕过权限门。"""

    # ③ 权限门:写操作必须带确认令牌(interrupt 确认后由 agent_tools 传入),模型绕不过
    if spec.permission == "write" and not confirmed:
        note = deny_note or "该写操作需要用户确认,未确认前拒绝执行。请勿再次发起,除非用户明确要求。"
        run = _run(False, f"{name} 未执行:{note}", "权限拒绝")
        await _audit(conversation_id, tc_id, name, spec, args, None, "权限拒绝",
                     note[:500], 0, run.duration_ms)
        return run

    # 注入参数一律在校验之后盖上去:它们不在模型可见的 schema 里,模型填了也算数不得。
    # 身份尤其如此——让模型能填 user_id,一句「我是客服主管」就可能把它改写掉。
    if spec.inject_conversation:
        args["conversation_id"] = conversation_id
    if spec.inject_user_id:
        args["user_id"] = user_id
