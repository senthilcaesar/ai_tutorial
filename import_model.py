from ollama import chat

response = chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'Hello!'}],
)
print(response.message.content)



from langchain_ollama import ChatOllama

# Initialize with your local Ollama model
local_llm = ChatOllama(
    model="llama3.1",  # Name of your model in Ollama
    temperature=0.7,
    num_predict=2048,
)

# Use it directly
response = local_llm.invoke("What is the capital city of Massachusetts?")
print(response.content)
