# Real-time LLM-empowered avatar with AI Search enhancement

## 1. Overview

- **Web:** The interface to provide user LLM-based avatar in browser.
- **Server:** The proxy to let frontend query LLM with AI Search enhancement.

## 2. How to start?

### Server

1. To run server successfully, 4 Azure resources are prerequisties:
    - Document Intelligence
    - AI Search
    - Azure OpenAI
    - Storage Account (Blob Storage)

2. Place your resource information and credential in `.env`, following `.env.example`

    ```
    DOC_INTELLIGENCE_ENDPOINT=
    DOC_INTELLIGENCE_KEY=

    AI_SEARCH_ENDPOINT=
    AI_SEARCH_KEY=

    AZURE_OPENAI_ENDPOINT=
    AZURE_OPENAI_KEY=
    AZURE_OPENAI_API_VERSION=
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT=
    AZURE_OPENAI_TEXT_DEPLOYMENT=

    BLOB_CONNECTION_STRING=
    ```
3. Install required libraries.
    ```
    cd server
    python -m venv venv

    source venv/scripts/activate    // Unix-Like
    ./venv/scripts/activate.ps1     // Windows
    
    pip install -r requirements.txt
    ```
4. Run the server
    ```
    uvicorn.exe main:app --host 0.0.0.0 --port 80
    ```

### Web
1. Below resource are required to activate avatar:
    - Speech Service (In Azure AI Service)
2. Open `basic.html`
    1. Choose the region of your Speech Service in select menu 
    2. Plcae the API key of your Speech Service
    3. Start Session