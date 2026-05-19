from Market_Research_Agent.connections import graph

def market_research(name,description,pricing,innovations):

    response=graph.invoke({'product_name':name,
                        'description':description,
                        'pricing':pricing,
                        'innovations':innovations,
                        'queries':[],
                        'search_results':[],
                        'report':''
                            
                        })
    
    return response['report']