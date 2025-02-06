import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    class AiSearch:
        ENDPOINT = os.getenv("AI_SEARCH_ENDPOINT")
        KEY = os.getenv("AI_SEARCH_KEY")

    class DocumentIntelligence:
        ENDPOINT = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
        KEY = os.getenv("DOC_INTELLIGENCE_KEY")

    class AzureOpenAi:
        ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        KEY = os.getenv("AZURE_OPENAI_KEY")

    class BlobStorage:
        CONN_STR = os.getenv("BLOB_CONNECTION_STRING")

config = Config()