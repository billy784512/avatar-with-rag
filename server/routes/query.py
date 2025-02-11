from fastapi import APIRouter

from utils.config import config
from utils.model import QueryItem
from services.ai_search_service import AiSearchService

router = APIRouter()
ai_search_service = AiSearchService(config.AiSearch.ENDPOINT, config.AiSearch.KEY, "paper-idx")

@router.get("/")
def hello():
    return {"message": "Hello, FastAPI!"}

@router.post("/query", status_code=200)
async def query_with_ai_search(req: QueryItem):
    combined_results= ai_search_service.query_documents(req.query, search_type=req.type, query_language=req.language)  
    openai_response = ai_search_service.query_openai(req.query, combined_results)

    result = openai_response['choices'][0]['message']['content']
    print(result)
    return {"result": result}