# 摘自 mcp_servers/logistics_server.py 第 21-38 行
# 仅用于面试核验，不是完整文件

@mcp.tool()
async def query_logistics(
    tracking_no: Annotated[str, Field(description="物流单号(形如 SF 开头),需先用 query_order 查订单拿到该单号")],
) -> dict:
    """用物流单号(tracking_no)查询物流状态、当前位置和轨迹。用于用户询问物流/快递到哪了时。
    物流单号不是订单号,需先用 query_order 查订单拿到 tracking_no,再调用本工具。"""
    if _DELAY > 0:
        await asyncio.sleep(_DELAY)
    rng = random.Random(f"logistics:{tracking_no}")      # 种子固定 → 同单号稳定
    code = rng.choice(_STATUS_CODES)
    city = rng.choice(_CITIES)
    return {
        "tracking_no": tracking_no,
        "status_code": code,                              # 内部枚举码,Server 侧不翻译,交 client 侧治理
        "current_city": city,
        "trace": [f"{city}分拨中心 已发出", f"内部状态码:{code}"],
        "carrier_code": "SF-EXP-01",                      # 内部承运商编码(回答用不上,client 侧应剔除)
    }
