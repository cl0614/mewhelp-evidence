# 摘自 app/tools/mcp_client.py 第 20-24 行、第 41-42 行
# 仅用于面试核验，不是完整文件

def _fmt_logistics(d: dict) -> dict:
    return {"tracking_no": d.get("tracking_no"),
            "status": _translate({"PICKED_UP": "已揽件", "IN_TRANSIT": "运输中",
                                  "DELIVERING": "派送中", "DELIVERED": "已签收"}, d.get("status_code")),
            "current_city": d.get("current_city"), "trace": d.get("trace")}


FORMATTERS = {"query_logistics": _fmt_logistics, "query_warranty": _fmt_warranty,
              "query_return_status": _fmt_return}
