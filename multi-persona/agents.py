from langgraph.graph import START,END,StateGraph
from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages

llm=ChatGroq(
    model='llama-3.1-8b-instant',

    api_key='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'
)

class State(TypedDict):
    name:str
    description:str
    pricing:str
    product:str
    reviews:dict
    summary:str
    

#Product summarising agent
def product_analyzer(state:State):
    name=state['name']
    description=state['description']
    pricing=state['pricing']

    res=llm.invoke(f'''
You are a Product Summarizer Agent in a multi-agent synthetic consumer testing system.

The user will provide raw product details such as features, pricing, audience, benefits, problems solved, and notes.

Your job is to convert that messy input into a clean, concise product brief that synthetic customer personas can easily understand and evaluate.

INPUT:
{name},{description},{pricing}

Return only:

Product Name:
Category:
What It Is:

Short Summary:
(2-3 sentence neutral summary for persona agents)

Keep it clear, short, neutral, and realistic. Do not add hype.

''')
    
    return {'product':res.content}

personas = {
    "student": """
19-year-old college student. Tight budget, busy classes, likes practical things.
Would you buy this? Why or why not?
""",

    "office_worker": """
28-year-old office employee. Values time, convenience, and reliability.
Would this improve daily life?
""",

    "budget_mom": """
35-year-old mother managing family expenses carefully.
Is this truly worth the money?
""",

    "tech_guy": """
24-year-old gadget lover who buys cool new tech early.
Is this exciting or average?
""",

    "skeptic": """
31-year-old careful buyer who distrusts hype and ads.
What feels unnecessary, risky, or overpriced?
"""
}


def synthetic_user(name,personality,product):
    prompt=f'''You are {name}, having personality of {personality}.

Review this product:{product} 

honestly answer in a natural human tone:
- First impression
- What you like
- What you dislike
- Would you buy it or ignore it
- Final short opinion

'''
    res=llm.invoke(prompt)

    return res.content

def synthetic_agent(state:State):
    product=state['product']
    res={}

    for name,personality in personas.items():
        result=synthetic_user(name,personality,product)
        res[name]=result
    
    return {'reviews':res}


def report_generator(state:State):
    reviews=state['reviews']
    product=state['product']
    str_reviews=str(reviews)

    report_prompt = f"""
    You are a Product Insight Analyst.

    Use the product details and synthetic user reviews to create one clear report in markdown format.

    PRODUCT:
    {product}

    REVIEWS:
    {str_reviews}

    Return:

    1. Overall Reaction
    2. Most Loved Features
    3. Biggest Concerns
    4. Best Customer Types
    5. Likely Rejecters
    6. Pricing Perception
    7. Product-Market Fit Score (/10 + reason)

    Be realistic, concise, and business-focused not too long.
    """
    res=llm.invoke(report_prompt)

    return {'summary':res.content}


def report_writer(state:State):
    report=state['summary']
    with open('report.md','w') as f:
        f.write(report)
    return {}
    



