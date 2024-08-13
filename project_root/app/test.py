from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from sympy import sympify

# 加载环境变量
load_dotenv()


# 定义数学工具类
class MathTool(BaseTool):
    def __init__(self, name="math_tool", description="Performs mathematical computations"):
        super().__init__(name=name, description=description)

    def _run(self, input_str):
        # 这个方法应该实现具体的工具逻辑
        try:
            # 使用 sympy 解析和计算表达式
            result = sympify(input_str).evalf()
            print('工具调用中')
            return str(result)  # 返回字符串形式的结果
        except Exception as e:
            # 处理任何可能的异常，并返回错误信息
            return f"Error: {e}"

    def __call__(self, query: str):
        # 这个方法允许类的实例表现得像函数一样，可以直接调用
        return self._run(query)


# 创建数学工具实例
math_tool = MathTool()

# 创建包含我们将使用的数学工具的列表
tools = [math_tool]

# 创建聊天模型实例
chat_model = ChatOpenAI(
    base_url='http://localhost:11434/v1/',
    model="llama3.1",
    api_key='ollama'
)

# 定义聊天提示模板
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个智能助手。你可能不需要为每个查询使用工具 - 用户可能只是想聊天！"),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# 创建一个聊天智能体，它结合了聊天模型和工具
agent = create_openai_tools_agent(chat_model, tools, prompt_template)

# 创建一个执行器来运行智能体
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 运行智能体并获取响应
response = executor.invoke({"messages": [HumanMessage(content="你好，你叫什么名字？")]})

# 打印响应
print(response)

# 测试数学工具功能
math_query = "2 + 2"
math_response = executor.invoke({"messages": [HumanMessage(content=math_query)]})
print(math_response)
