# 摘自 app/tools/builtin/orders.py 第 10-25 行、第 42-43 行
# 仅用于面试核验，不是完整文件

# 查不到和不是本人的单回同一句话。分开回就成了枚举 oracle:攻击者靠回答差异
# 就能挨个试出哪些订单号真实存在。
NOT_OWNED = {"error": "没有找到您的这笔订单", "code": "order_not_owned"}


@tool
async def query_order(
    order_id: Annotated[str, Field(description="订单号,例如 1001")],
    user_id: Annotated[str, InjectedToolArg],
) -> dict:
    """查询订单的状态、金额、下单时间、商品名和物流单号(tracking_no)。"""
    if not owns_order(user_id, order_id):
        return dict(NOT_OWNED)
    return order_snapshot(order_id)


registry.register(registry.spec_from_langchain_tool(
    query_order, source="builtin", inject_user_id=True))
