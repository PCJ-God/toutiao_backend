from typing import AsyncIterator, List

from langgraph.graph import END, START, StateGraph

from config.ai_conf import llm

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from schemas.ai import ChatState


def _convert_to_lc(messages):
    return [HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content) for m in messages]


# 2. 定义节点函数 —— 每个节点是一个处理步骤
async def call_llm_node(state: ChatState) -> dict:
    """调用 LLM，把回复写入 state"""

    result = await llm.ainvoke(state["messages"]) # type: ignore
    return {"response": result.content, "messages": [result]}

# 3. 构建 Graph
def build_chat_graph():
    builder = StateGraph(ChatState)

    builder.add_node("chat", call_llm_node)  # 注册节点
    builder.add_edge(START, "chat")           # 开始 → chat
    builder.add_edge("chat", END)             # chat → 结束

    return builder.compile()


# 4. 对外暴露的流式接口
async def stream_chat(messages: list) -> AsyncIterator[str]:
    graph = build_chat_graph()

    # astream_events 可以逐 token 输出
    async for event in graph.astream_events(
        {"messages": _convert_to_lc(messages)}, # type: ignore
        version="v2",
    ):
        kind = event.get("event")
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content # type: ignore
            if content:
                yield content