from Multi_Persona_System.connections import graph

def multi_persona(name,description,pricing,innovations):
    result=graph.invoke({'name':name,'description':description,'pricing':pricing,'innovations':innovations})

    return result['summary']

