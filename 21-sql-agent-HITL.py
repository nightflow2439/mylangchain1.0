from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
  model="deepseek:deepseek-chat",
  temperature=0.1
)

import requests, pathlib

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

print(f"Dialect: {db.dialect}")
print(f"Available tables: {db.get_usable_table_names()}")
print(f'Sample output: {db.run("SELECT * FROM Artist LIMIT 5;")}')

from langchain_community.agent_toolkits import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=model)

tools = toolkit.get_tools()

for tool in tools:
    print(f"{tool.name}: {tool.description}\n")

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect=db.dialect,
    top_k=5,
)

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"sql_db_query": True},
            description_prefix="Tool execution pending approval",
        ),
    ],
    checkpointer=InMemorySaver(),
)

question = "Which genre on average has the longest tracks?"
config = {"configurable": {"thread_id": "1"}}

printed_ids = set()

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    config,
    stream_mode="values",
):
    if "__interrupt__" in step:
        print("INTERRUPTED:")
        interrupt = step["__interrupt__"][0]
        for request in interrupt.value["action_requests"]:
            print(request["description"])
    if "messages" in step:
        # step["messages"][-1].pretty_print()
        msg = step["messages"][-1]
        msg_id = getattr(msg, "id", None)
        if msg_id not in printed_ids:
            printed_ids.add(msg_id)
            msg.pretty_print()

from langgraph.types import Command

query_count = 0

while True:
    query_count += 1
    print(f"\n这是第 {query_count} 次 SQL 查询请求。")
    user_input = input("是否批准执行？(y=批准/ n=拒绝并终止): ").strip().lower()

    if user_input == "n":
        print("已拒绝，终止 agent。")
        break
    else:
        command = Command(resume={"decisions": [{"type": "approve"}]})

    interrupted = False

    for step in agent.stream(
        command,
        config,
        stream_mode="values",
    ):
        print("--------------")
        print(f"DEBUG step keys: {list(step.keys())}")
        print("--------------")
        if "messages" in step:
            # step["messages"][-1].pretty_print()
            msg = step["messages"][-1]
            msg_id = getattr(msg, "id", None)
            if msg_id not in printed_ids:
                printed_ids.add(msg_id)
                msg.pretty_print()
        if "__interrupt__" in step:
            print("INTERRUPTED:")
            interrupt = step["__interrupt__"][0]
            for request in interrupt.value["action_requests"]:
                print(request["description"])
            interrupted = True

    if not interrupted:
        break