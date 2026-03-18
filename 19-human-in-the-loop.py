from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime

from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command

from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT = """
  You are an excellent comedian. You always answer the audience's question in humorous ways.

  You have access to two tool.

  - get_person_information: use this to get information about a person so that you can
    talk about him/her
  - get_person: use this to get the person
  
  First you use get_person to get the person that you will talk about, then you use get_person_information to find out if you have any information about the person.
  If you do, naturally bring up some of the information in humorous way, and you don't have to bring up all of the information.
  If you do not, just continue the conversation with a pun.

  用中文回答
"""

@tool
def get_person_information(person: str) -> str:
  """Get information about a person"""
  if person == "邵昱衡":
    return ["外号是邵老鸡", "外号是老烧鸡", "外号是91邵"]
  elif person == "彭傲然":
    return ["喜欢机电妹", "喜欢韦思羽","机电妹就是韦思羽", "许舒娜喜欢彭傲然", "朱婉婷的舔狗"]
  elif person == "费亦铭":
    return ["喜欢刘芷廷", "喜欢许舒娜"]
  
@dataclass
class Context:
  """Custom runtime contect schema"""
  person_id: str

@tool
def get_person(runtime: ToolRuntime[Context]) -> str:
  """Get the person based on person ID"""
  person_id = runtime.context.person_id
  if person_id == "1":
    return "邵昱衡"
  if person_id == "2":
    return "彭傲然"
  if person_id == "3":
    return "费亦铭"
  else:
    return "韦思羽"
  
@dataclass
class ResponseFormat:
  """Response format for the agent"""
  punny_response: str
  person: str

checkpointer = InMemorySaver()

agent = create_agent(
  model="deepseek:deepseek-chat",
  system_prompt=SYSTEM_PROMPT,
  tools=[get_person_information, get_person],
  middleware=[
    HumanInTheLoopMiddleware(
      interrupt_on={
        "get_person": True,
        "get_person_information": {
          "allowed_decisions": ["approve", "reject"]
        }
      },
      description_prefix="工具执行挂起等待决策"
    )
  ],
  context_schema=Context,
  response_format=ResponseFormat,
  checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
  {"messages": [{"role": "user", "content": "Make some jokes about his nickname."}]},
  config=config,
  context=Context(person_id="1")
)

# print(response["structured_response"].punny_response)

messages = response["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
  message.pretty_print()

# 决策1
if "__interrupt__" in response: # dict, 判断response是否有key: __interrupt__
  print("INTERRUPTED")
  interrupt = response["__interrupt__"][0]
  for request in interrupt.value["action_requests"]:
    print(request["description"])

response = agent.invoke(
  Command(
    resume={"decisions": [
      {"type": "approve"}
    ]}
  ),
  config=config,
  context=Context(person_id="1")
)

messages = response["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
  message.pretty_print()

# 决策2
if "__interrupt__" in response: # dict, 判断response是否有key: __interrupt__
  print("INTERRUPTED")
  interrupt = response["__interrupt__"][0]
  for request in interrupt.value["action_requests"]:
    print(request["description"])

response = agent.invoke(
  Command(
    resume={"decisions": [
      {"type": "approve"}
    ]}
  ),
  config=config,
  context=Context(person_id="1")
)

messages = response["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
  message.pretty_print()