import uuid

from dataclasses import dataclass, field

from src.agents.registry import Configuration
from src.agents.tools_factory import get_all_tools

# @dataclass是 Python 中的一个装饰器，用于简化类的定义，并自动生成一些常用方法（如 __init__、__repr__ 等）。
# 其中，kw_only=True 参数表示所有字段必须通过关键字参数传递，不能通过位置参数传递。
@dataclass(kw_only=True)
class ChatbotConfiguration(Configuration):
    """Chatbot 的配置

    配置说明：

    metadata 中 configurable 为 True 的配置项可以被用户配置，
    configurable 为 False 的配置项不能被用户配置，只能由开发者预设。
    """

    system_prompt: str = field(
        default="You are a helpful assistant.",
        metadata={
            "name": "系统提示词",
            "configurable": True,
            "description": "用来描述智能体的角色和行为"
        },
    )

    model: str = field(
        #default="siliconflow/Qwen/Qwen3-8B", #"zhipu/glm-4-plus", 这个值可以被分为分解为provider/model，后面通过provider来决定如何调用模型
        default="dashscope/qwen3-235b-a22b",
        metadata={
            "name": "智能体模型",
            "configurable": True,
            "options": [],
            "description": "智能体的驱动模型"
        },
    )

    tools: list[str] = field(
        default_factory=list,
        metadata={
            "name": "工具",
            "configurable": True,
            "options": list(get_all_tools().keys()),  # 这里的选择是所有的工具
            "description": "工具列表"
        },
    )
