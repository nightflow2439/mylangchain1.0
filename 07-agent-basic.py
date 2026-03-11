from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

agent = create_agent(
  model="deepseek:deepseek-chat"
)

# print(agent)
# <langgraph.graph.state.CompiledStateGraph object at 0x000001EB1D6AD650>

# print(agent.nodes)
# {
# '__start__': <langgraph.pregel._read.PregelNode object at 0x000001D4A544DFD0>, 
# 'model': <langgraph.pregel._read.PregelNode object at 0x000001D4A544E290>
# }

results = agent.invoke({"messages":[{"role": "user", "content": "What is the weather like in SF"}]})
# print(results)
# {'messages': [
# HumanMessage(content='What is the weather like in SF', additional_kwargs={}, response_metadata={}, id='a995b53f-e8f4-41c1-be07-869ec6fd9546'), 
# AIMessage(content='As of my last update, I don\'t have real-time data access. However, I can give you a general idea of San Francisco\'s weather patterns and suggest how to get the current forecast.\n\n### **Typical San Francisco Weather (General Patterns):**\n*   **"Fogust" and Microclimates:** San Francisco is famous for its microclimates. While it can be sunny and warm in neighborhoods like the Mission or SoMa, the Sunset and Richmond districts (and the Golden Gate Bridge) are often cool, windy, and foggy, especially in summer.\n*   **Seasonal Quirk:** Summers are often **cool and foggy**, with highs in the 60s°F (15-20°C). The warmest months are usually September and October.\n*   **Winters** are mild and rainy, with daytime temperatures in the 50s-60s°F (10-15°C). It rarely freezes or snows.\n*   **Layering is Key:** The saying "The coldest winter I ever spent was a summer in San Francisco" (often misattributed to Mark Twain) exists for a reason. Always bring a jacket, even on a sunny summer day.\n\n### **How to Get the Current Weather:**\nFor the most accurate, up-to-the-minute forecast, I recommend checking:\n1.  **Weather Websites/Apps:** [Weather.com](https://weather.com), [AccuWeather](https://www.accuweather.com), or your smartphone\'s weather app.\n2.  **Search:** Try a quick web search for **"San Francisco weather"** for an instant forecast.\n\nWould you like me to help you find something specific based on the weather, like typical activities for the season?', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 361, 'prompt_tokens': 11, 'total_tokens': 372, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 11}, 'model_provider': 'deepseek', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': 'dfe9f581-6aaf-4a3d-9a4c-c4081b0eeaad', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019cdbdc-7bc6-75a2-83fb-baf9b0c8d362-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 11, 'output_tokens': 361, 'total_tokens': 372, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}})
# ]}

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
  message.pretty_print()