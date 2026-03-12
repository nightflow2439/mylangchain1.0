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

# for event in agent.stream(
#   {"messages":[{"role": "user", "content": "What is the weather like in SF"}]},
#   stream_mode="values" # message by message
# ):
#   messages = event["messages"]
#   print(f"历史消息：{len(messages)}条")
#   # for message in messages:
#   #   message.pretty_print()
#   messages[-1].pretty_print()

for chunk in agent.stream(
  {"messages":[{"role": "user", "content": "What is the weather like in SF"}]},
  stream_mode="messages" #token by token
):
  print(chunk[0].content, end='')
# (AIMessageChunk(
# content='', 
# additional_kwargs={}, 
# response_metadata={'model_provider': 'deepseek'}, 
# id='lc_run--019cdc60-aa3e-7790-982a-d7ca04091d2b', 
# tool_calls=[], 
# invalid_tool_calls=[], 
# tool_call_chunks=[]), 
# {'langgraph_step': 1, 
# 'langgraph_node': 'model', 
# 'langgraph_triggers': ('branch:to:model',), 
# 'langgraph_path': ('__pregel_pull', 'model'), 
# 'langgraph_checkpoint_ns': 'model:4897ef8d-9f48-2f80-c635-52a63205b8be', 
# 'checkpoint_ns': 'model:4897ef8d-9f48-2f80-c635-52a63205b8be', 
# 'ls_provider': 'deepseek', 
# 'ls_model_name': 'deepseek-chat', 
# 'ls_model_type': 'chat', 
# 'ls_temperature': None}
# )