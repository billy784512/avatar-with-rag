import requests
from typing import List, Dict

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    QueryType,
    QueryCaptionType,
    QueryAnswerType,
    VectorizableTextQuery
)

from utils.config import config

class AiSearchService():

    def __init__(self, endpoint: str, key: str, index_name: str) -> None:
        credential = AzureKeyCredential(key)
        
        self.search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
        self.return_docs_num = 1
        self.setup_openai_info()

    def setup_openai_info(self) -> None:
        self.opei_ai_info = {
            "azure_openai_endpoint": config.AzureOpenAi.ENDPOINT,
            "azure_openai_key": config.AzureOpenAi.KEY,
            "azure_openai_api_version": config.AzureOpenAi.API_VERSION,
            "azure_openai_embedding_deployment": config.AzureOpenAi.EMBEDDING_DEPLOYMENT,
            "text_deployment_name": config.AzureOpenAi.TEXT_DEPLOYMENT
        }

    def query_documents(self, query: str, search_type: str='semantic', query_language: str="zh-tw") -> List[Dict]:

        vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="content_vector")
  
        # three types: vector, semantic, hybrid
        if search_type == 'vector':  
            results = self.search_client.search(    
                search_text=None,    
                vector_queries=[vector_query],  
                select=["header_1","header_2","header_3","file_name", "doc_url", "contents"],  
                top=self.return_docs_num
            )  
        elif search_type == 'hybrid':  
            results = self.search_client.search(    
                search_text=query,    
                vector_queries=[vector_query],  
                select=["header_1","header_2","header_3","file_name", "doc_url", "contents"], 
                top=self.return_docs_num
            )  
        else:  
            results = self.search_client.search(    
                search_text=query,    
                vector_queries=[vector_query],  
                select=["header_1","header_2","header_3","file_name", "doc_url", "contents"],
                query_type=QueryType.SEMANTIC, semantic_configuration_name='my-semantic-config', query_caption=QueryCaptionType.EXTRACTIVE, query_answer=QueryAnswerType.EXTRACTIVE,  
                top=self.return_docs_num,
                search_fields= ["contents"],  
                query_rewrites= "generative|count-5",  
                query_language = query_language      
            )  
    
        combined_results = []  
        for result in results:    
            # logic for section_headers: header_3 --> header_2 --> header_1
            section_headers = result['header_3'] or result['header_2'] or result['header_1']    

            combined_result = {  
                'file_name': result['file_name'],  
                'contents': result['contents'],  
                'doc_url': result['doc_url'], 
                'section_headers': section_headers
            }  
            combined_results.append(combined_result)    
    
        return combined_results
    
    def query_openai(self, user_input:str, combined_results: List[Dict]) -> Dict:
        val1 = self.opei_ai_info.get("azure_openai_endpoint")
        val2 = self.opei_ai_info.get("text_deployment_name")
        val3 = self.opei_ai_info.get("azure_openai_api_version")
        base_url = f"{val1}openai/deployments/{val2}" 

        headers = {   
            "Content-Type": "application/json",   
            "api-key": self.opei_ai_info.get("azure_openai_key") 
        } 
        
        # Prepare endpoint and request body
        endpoint = f"{base_url}/chat/completions?api-version={val3}"  # The endpoint for making execution requests

        system_prompt = """  
        Utilize emojis when responding to Chi-Chat inquiries. As an AI assistant, your primary functions are to provide answers based on a Knowledge Base, fetch weather data, and retrieve specific file contents.  
        
        Query documents, attribute sources accurately. Start your response by citing each source within individual square brackets, including the section header for clarity. For example, use "[folder3/info343 - Section Name](http://wikipedia.com)" instead of just "[folder3/info343,http://wikipedia.com]." Structure your answers as follows:  
        
        - Answer: [file_name1 - Section Header1][file_name2 - Section Header2](Insert the answer content here, based on the referenced facts or information.)  
        
        - Ensure URLs are in markdown format, e.g., [file_name - Section Header](doc_url).  
        
        ### General Instructions:  
        - Follow the user's input language when responding.  
        - Utilize emojis appropriately to enhance engagement in Chi-Chat inquiries.  
        
        Please ensure to use the appropriate function based on the user's query and the context provided. Again, follow the user's input language when responding.  
        """  


        for result in combined_results:
            system_prompt += f"File Name: {result['file_name']}\n"
            system_prompt += f"Section Name: {result['section_headers']}\n"
            system_prompt += f"Source URL: {result['doc_url']}\n"
            system_prompt += f"Contents: {result['contents']}\n\n"


        data = { 
            "messages": [ 
                { "role": "system", "content": system_prompt}, 
                { "role": "user", "content": user_input }
            ], 
            "max_tokens": 750,
            "temperature": 0,
        }   

        response = requests.post(endpoint, headers=headers, json=data)
        
        if response.status_code != 200:
            return {"error": response.text}
        
        return response.json()