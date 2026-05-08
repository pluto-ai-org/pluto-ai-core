from agents import product_analyzer,synthetic_agent,report_generator,report_writer,State
from langgraph.graph import START,StateGraph,END
import streamlit as st



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

st.title('Multi-Persona System Demo')

name=st.text_input('What is you product?')
description=st.text_area('Tell us more about your product')
pricing=st.text_input('What is the price range of your product?')

if st.button('Launch!'):
    result=graph.invoke({'name':name,'description':description,'pricing':pricing})
    st.markdown(result['summary'])