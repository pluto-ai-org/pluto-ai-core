from agents import product_analyzer,synthetic_agent,report_generator,report_writer,State
from langgraph.graph import START,StateGraph,END

builder=StateGraph(State)

builder.add_node('analyzer',product_analyzer)
builder.add_node('persona',synthetic_agent)
builder.add_node('report_gen',report_generator)
builder.add_node('writer',report_writer)

builder.add_edge(START,'analyzer')
builder.add_edge('analyzer','persona')
builder.add_edge('persona','report_gen')
builder.add_edge('report_gen','writer')
builder.add_edge('writer',END)

graph=builder.compile()

result=graph.invoke({})

print('----PRODUCT ANALYZER-----')
print(result['product'])
print('----REPORT-----')
print(result['summary'])

report=result['summary']