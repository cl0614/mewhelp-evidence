# 摘自 app/tools/registry.py 第 13-31 行
# 仅用于面试核验，不是完整文件

# 权限我们侧独裁:写清单按名字定;未登记(含所有 MCP)工具一律按只读放行。
WRITE_TOOLS: set[str] = {"create_ticket"}


@dataclass
class ToolSpec:
    name: str
    description: str
    json_schema: dict            # 参数 JSON Schema(校验用;模型可见口径,不含注入参数)
    tool: BaseTool
    permission: str              # "read" | "write"
    source: str                  # "builtin" | "mcp"
    mcp_server: str | None = None
    timeout: float | None = None
    max_retries: int | None = None
    inject_conversation: bool = False
    inject_user_id: bool = False
    format_result: Callable[[dict], dict] | None = None
