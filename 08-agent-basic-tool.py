from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

def get_weather(city: str) -> str:
  """get weather for a given city"""
  return f"It's always sunny in {city}!"

agent = create_agent(
  model="deepseek:deepseek-chat",
  tools=[get_weather]
)

print(agent.nodes)

# {
# '__start__': <langgraph.pregel._read.PregelNode object at 0x000001D8C7F7A550>, 
# 'model': <langgraph.pregel._read.PregelNode object at 0x000001D8C7F7A7D0>, 
# 'tools': <langgraph.pregel._read.PregelNode object at 0x000001D8C7F6AB10>
# }

# results = agent.invoke({"messages":[{"role": "user", "content": "What is the weather like in SF"}]})

# messages = results["messages"]
# print(f"历史消息：{len(messages)}条")
# for message in messages:
#   message.pretty_print()