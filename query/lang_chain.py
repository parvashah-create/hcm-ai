from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
import openai
import os



class GraphChain:
    def __init__(self, url, username, password, openai_api_key) -> None:
        self.graph = Neo4jGraph(url=url, username=username, password=password)
        self.openai_api_key = openai_api_key

    def graph_qa(self, prompt):
        chain = GraphCypherQAChain.from_llm(ChatOpenAI(temperature=0), graph=self.graph, verbose=True)
        response = chain.run(prompt)
        return response
