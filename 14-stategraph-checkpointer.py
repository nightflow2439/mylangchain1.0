## checkpointer: 检查点管理器
## checkpoint: 检查点，状态图的总体状态快照

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

# 整个状态图的状态
class State(TypedDict):
  foo: str
  bar: Annotated[list[str], add]

def node_a(state: State):
  return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
  return {"foo": "b", "bar": ["b"]}

# 构建状态图
workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

# 检查点管理器
checkpointer = InMemorySaver()

# 运行
graph = workflow.compile(checkpointer=checkpointer)


# 配置
config: RunnableConfig = {
  "configurable": {"thread_id": "1"}
}

# 调用
results = graph.invoke({"foo":""}, config)
print(results)
# {'foo': 'b', 'bar': ['a', 'b']}

# 状态查看
# print(graph.get_state(config))
# StateSnapshot(
#   values={'foo': 'b', 'bar': ['a', 'b']}, 
#   next=(), 
#   config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f11eb78-24f2-68a6-8002-c28465555a56'}}, 
#   metadata={'source': 'loop', 'step': 2, 'parents': {}}, 
#   created_at='2026-03-13T08:34:53.927030+00:00', 
#   parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f11eb78-24f2-68a5-8001-c19ee44cfae2'}}, 
#   tasks=(), 
#   interrupts=()
# )

for checkpoint_tuple in checkpointer.list(config):
  print()
  print(checkpoint_tuple[2]["step"])
  print(checkpoint_tuple[2]["source"])
  print(checkpoint_tuple[1]["channel_values"])
  # print(checkpoint_tuple)
# CheckpointTuple(
#   config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f11eb7e-3255-62ec-8002-d3ed8a61a21a'}}, 
#   checkpoint={
#     'v': 4, 
#     'ts': '2026-03-13T08:37:36.391857+00:00', 
#     'id': '1f11eb7e-3255-62ec-8002-d3ed8a61a21a', 
#     'channel_versions': {
#       '__start__': '00000000000000000000000000000002.0.21716367473049392', 
#       'foo': '00000000000000000000000000000004.0.5303312100328963', 
#       'branch:to:node_a': '00000000000000000000000000000003.0.5722114706308457', 
#       'bar': '00000000000000000000000000000004.0.5303312100328963', 
#       'branch:to:node_b': '00000000000000000000000000000004.0.5303312100328963'
#      }, 
#     'versions_seen': {
#       '__input__': {}, 
#       '__start__': {'__start__': '00000000000000000000000000000001.0.3524449321870139'}, 
#       'node_a': {'branch:to:node_a': '00000000000000000000000000000002.0.21716367473049392'}, 
#       'node_b': {'branch:to:node_b': '00000000000000000000000000000003.0.5722114706308457'}
#     }, 
#     'updated_channels': ['bar', 'foo'], 
#     'channel_values': {'foo': 'b', 'bar': ['a', 'b']}
#   }, 
#   metadata={
#     'source': 'loop', 
#     'step': 2, 
#     'parents': {}}, 
#     parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f11eb7e-3252-6bbb-8001-3191e005b15a'}
#   }, 
#   pending_writes=[]
# )

