from agents import query_gen,search_agent,report_gen,report_writer,State
from langgraph.graph import START,END,StateGraph

builder=StateGraph(State)

builder.add_node('query',query_gen)
builder.add_node('search',search_agent)
builder.add_node('report',report_gen)
builder.add_node('writer',report_writer)

builder.add_edge(START,'query')
builder.add_edge('query','search')
builder.add_edge('search','report')
builder.add_edge('report','writer')
builder.add_edge('writer',END)

graph=builder.compile()

name=input('Enter Product name:')
description=input('Say more about your product:')
pricing=input('Tell us about your pricing:')
innovations=input('What are the innovations in your product:')

response=graph.invoke({'product_name':name,
                       'description':description,
                       'pricing':pricing,
                       'innovations':innovations,
                       'queries':[],
                       'search_results':[],
                       'report':''
                        
                       })

print('--------QUERIES---------')
print(response['queries'])
print('------------SEARCH RESULT------------')
print(response['search_results'])
