## 消息列表的内存管理
## 通过 config 实现多会话管理

from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv

load_dotenv()
DB_URI = "postgresql://postgres:141592@localhost:5432/postgres?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
  # checkpointer.setup() # 创建数据表，只运行一次

  agent = create_agent(
    model="deepseek:deepseek-chat",
    checkpointer=checkpointer
  )

  config = {"configurable": {"thread_id": "1"}}

  # 第一轮问答

  # 问
  results = agent.invoke(
    {"messages":[{"role": "user", "content": "来一首宋词"}]},
    config=config  
  )

  # 答
  messages = results["messages"]
  print(f"历史消息：{len(messages)}条")
  for message in messages:
    message.pretty_print()

  # 第二轮问答

  # 问
  results = agent.invoke(
    {"messages": [{"role": "user", "content": "再来"}]},
    config=config
  )

  # 答
  messages = results["messages"]
  print(f"历史消息：{len(messages)}条")
  for message in messages:
    message.pretty_print()