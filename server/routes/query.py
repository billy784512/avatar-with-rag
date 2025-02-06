from fastapi import APIRouter

from utils.config import config
from services.ai_search_service import AiSearchService

router = APIRouter()
ai_search_service = AiSearchService(config.AiSearch.ENDPOINT, config.AiSearch.KEY, "paper-idx")

async def query_with_ai_search(query: str):
    combined_results= ai_search_service.query_documents(query, search_type='semantic',query_language='zh-tw')  
    openai_response = ai_search_service.query_openai(query, combined_results)

    # TODO: Http Response