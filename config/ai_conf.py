from langchain_openai import ChatOpenAI


BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = "sk-ws-H.EREDPEH.F8Q5.MEYCIQCdvr5z_1BfC4OgjIhMWp0UMOyTUNZvENlaTwTNSiKMfAIhAKFgvkvGla3YCS_rZT0OntrkFOJ91ULEFSBpyFZCEIog"
MODEL = "qwen3.8-max"  # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models


llm = ChatOpenAI(
    model=MODEL,
    base_url=BASE_URL,
    api_key=API_KEY, # type: ignore
    streaming=True
)