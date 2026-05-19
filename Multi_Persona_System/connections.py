from Multi_Persona_System.agents import product_analyzer,synthetic_agent,report_generator,State
from langgraph.graph import START,StateGraph,END

builder=StateGraph(State)

builder.add_node('analyzer',product_analyzer)
builder.add_node('persona',synthetic_agent)
builder.add_node('report_gen',report_generator)


builder.add_edge(START,'analyzer')
builder.add_edge('analyzer','persona')
builder.add_edge('persona','report_gen')
builder.add_edge('report_gen',END)


graph=builder.compile()



