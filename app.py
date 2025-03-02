# import neccessary modules
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel


model = HfApiModel()
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)
query=input("Input the agent prompt: ")
response = agent.run(query)
print(response)
