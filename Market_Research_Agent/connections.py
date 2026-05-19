from Market_Research_Agent.agents import query_gen,search_agent,report_gen,State
from langgraph.graph import START,END,StateGraph

builder=StateGraph(State)

builder.add_node('query',query_gen)
builder.add_node('search',search_agent)
builder.add_node('report',report_gen)


builder.add_edge(START,'query')
builder.add_edge('query','search')
builder.add_edge('search','report')
builder.add_edge('report',END)


graph=builder.compile()




