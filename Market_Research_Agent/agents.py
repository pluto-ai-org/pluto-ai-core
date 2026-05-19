from langgraph.graph import START,END,StateGraph
from typing_extensions import TypedDict
from tavily import TavilyClient
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import ast

load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


llm=ChatGroq(
    model='llama-3.1-8b-instant',

    api_key=os.getenv('GROQ_API_KEY')
)

class State(TypedDict):
    product_name:str
    description:str
    pricing:str
    innovations:str
    queries:list
    search_results:list
    report:str

def query_gen(state:State):
    name=state['product_name']
    description=state['description']
    pricing=state['pricing']
    innovations=state['innovations']

    prompt=f'''
Generate 5 concise Tavily research queries.

Return ONLY a valid Python list using double quotes only.
No markdown.
No explanations.
No comments.

Example:
["query1", "query2"]

Product: {name}
Description: {description}
Pricing: {pricing}
Innovations: {innovations}'''
    
    result=llm.invoke(prompt)

    response=ast.literal_eval(result.content)

    return {'queries':response}

def search_agent(state:State):
    queries=state['queries']
    results=[]

    for query in queries:
        srch = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            include_answer=True,
            include_raw_content=False
        )

        results.append(srch['answer'])
    return {'search_results':results}

def report_gen(state:State):
    srch_results=str(state['search_results'])
    description=state['description']
    name=state['product_name']
    prompt=f'''Generate a concise markdown market research report using the provided research.

Include:
- Executive Summary
- Competitors
- Trends
- User Pain Points
- Pricing Insights
- Opportunities
- Risks
- Recommendations

Keep it analytical, structured, and actionable.
Use only the provided data.

product name: {name}
Product description:
{description}

Research:
{srch_results}'''
    
    res=llm.invoke(prompt)

    return{'report':res.content}

"""def report_writer(state:State):
    report=state['report']
    with open('market_research_report.md','w') as f:
        f.write(report)
    return {}"""
    

    
    


    