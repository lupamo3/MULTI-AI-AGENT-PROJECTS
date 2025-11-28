# app/backend/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.ai_agent import get_response_from_ai_agents
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

import traceback

logger = get_logger(__name__)
app = FastAPI()


class ChatRequest(BaseModel):
    model_name: str
    system_prompt: str | None = ""
    messages: list[str]
    allow_search: bool = False


@app.post("/chat")
async def chat(request: ChatRequest):
    # VERY VERBOSE DEBUG LOGGING
    print("\n========== /chat CALLED ==========", flush=True)
    print(f"model_name   = {request.model_name}", flush=True)
    print(f"allow_search = {request.allow_search}", flush=True)
    print(f"system_prompt = {request.system_prompt!r}", flush=True)
    print(f"messages     = {request.messages}", flush=True)
    print("==================================\n", flush=True)

    try:
        query_text = "\n".join(request.messages)

        response = get_response_from_ai_agents(
            llm_id=request.model_name,
            query=query_text,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt or "",
        )

        print(">>> /chat SUCCESS, response from agent:")
        print(response)
        print("==================================\n", flush=True)

        return {"response": response}

    except CustomException as e:
        print(">>> CustomException in /chat", flush=True)
        traceback.print_exc()
        logger.exception("CustomException in /chat")
        # expose error text so you can see it in Streamlit
        raise HTTPException(status_code=500, detail=f"CustomException: {e}")

    except Exception as e:
        print(">>> Unhandled Exception in /chat", flush=True)
        traceback.print_exc()
        logger.exception("Unhandled error in /chat")
        # expose REAL error for now (we’ll hide later)
        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {e}",
        )
