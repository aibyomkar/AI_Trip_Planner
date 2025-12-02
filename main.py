# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from utils.save_to_document import save_document
# from pydantic import BaseModel
# from agent.agentic_workflow import GraphBuilder
# from fastapi.responses import JSONResponse
# import os
# import datetime
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# # ✅ Root endpoint for GET and HEAD (for UptimeRobot)
# @app.get("/")
# @app.head("/")
# def root():
#     return JSONResponse(content={"status": "AI Trip Planner is running!", "version": "1.0"}, status_code=200)

# # ✅ CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['https://roamio.streamlit.app'],  # set specific origins in prod
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*']
# )

# # ✅ Pydantic model
# class QueryRequest(BaseModel):
#     query: str

# # ✅ Main POST endpoint
# @app.post("/query")
# async def query_travel_agent(request: QueryRequest):
#     try:
#         print(f"🔍 Received request: {request}")
#         print(f"🔍 Query content: {request.query}")
        
#         graph = GraphBuilder(model_provider='groq')
#         react_app = graph()

#         png_graph = react_app.get_graph().draw_mermaid_png()
#         with open('my_graph.png', 'wb') as f:
#             f.write(png_graph)
#         print(f'Graph saved as \'my_graph.png\' in {os.getcwd()}')

#         messages = {'messages': [request.query]}
#         output = react_app.invoke(messages)

#         if isinstance(output, dict) and 'messages' in output:
#             final_output = output['messages'][-1].content
#         else:
#             final_output = str(output)

#         return {'answer': final_output}

#     except Exception as e:
#         print(f"❌ Error details: {e}")
#         import traceback
#         print(f"❌ Full traceback: {traceback.format_exc()}")
#         return JSONResponse(status_code=500, content={'error': str(e)})











# main.py - robust FastAPI backend for Roamio (replace existing main.py)
import os
import time
import logging
import traceback
from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# load .env (local only) - Render will use environment variables set in dashboard
load_dotenv()

# ---------- logger ----------
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

# ---------- required envs (names only) ----------
REQUIRED_ENVS = [
    "GROQ_API_KEY",      # concierge provider / Groq (agent) key
    # add any other keys your code expects here, for detection only (we won't print values)
    # "OPENAI_API_KEY", "GOOGLE_API_KEY", "GPLACES_API_KEY", "OPENWEATHERMAP_API_KEY", ...
]

# Optional endpoint name your repo might expect
CONCIERGE_URL = os.getenv("CONCIERGE_URL") or os.getenv("GROQ_CONCIERGE_URL") or os.getenv("LANGGRAPH_URL")

missing = [k for k in REQUIRED_ENVS if not os.getenv(k)]
if missing:
    logger.warning("At startup: missing environment variables (names only): %s. Your app may fail.", missing)
else:
    logger.info("Environment variables present (masked).")

if not CONCIERGE_URL:
    # Not fatal here — GraphBuilder may still use only GROQ_API_KEY internally — but warn.
    logger.info("CONCIERGE_URL not set. If your agent expects a URL env var, set CONCIERGE_URL in Render.")

# ---------- small retry helper ----------
def retry_with_backoff(fn, max_attempts: int = 3, base_delay: float = 1.0, allowed_exceptions=(Exception,)):
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except allowed_exceptions as e:
            last_exc = e
            logger.warning("Attempt %d/%d failed: %s", attempt, max_attempts, repr(e))
            if attempt == max_attempts:
                logger.error("All %d attempts failed.", max_attempts)
                raise
            sleep_for = base_delay * (2 ** (attempt - 1))
            logger.info("Retrying after %.1f seconds...", sleep_for)
            time.sleep(sleep_for)
    raise last_exc

# ---------- app ----------
app = FastAPI(title="Roamio AI Trip Planner")

# CORS - keep your existing Streamlit origin (adjust if you test locally)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://roamio.streamlit.app'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Pydantic model
class QueryRequest(BaseModel):
    query: str

# Root
@app.get("/")
@app.head("/")
def root():
    return JSONResponse(content={"status": "AI Trip Planner is running!", "version": "1.0"}, status_code=200)

# Fallback plan - deterministic simple generator (guaranteed to work offline)
@app.post("/fallback_plan")
def fallback_plan(req: QueryRequest = Body(...)):
    try:
        prompt_text = req.query or ""
        # naive city extraction
        city = "your destination"
        tokens = [t.strip(",.") for t in prompt_text.split() if t.strip(",.")]
        for t in tokens[:5]:
            if len(t) > 2:
                city = t
                break
        plan = {
            "title": f"Quick 3-day plan for {city}",
            "summary": f"A minimal fallback itinerary for {city}. Verify all details before travel.",
            "days": {
                "Day 1": ["Arrive & check-in", "Visit a recommended local spot", "Dinner at a popular local place"],
                "Day 2": ["Morning activity", "Local market / cafe", "Sunset spot / viewpoint"],
                "Day 3": ["Relaxed morning", "Souvenir shopping", "Depart"]
            }
        }
        return {"status":"ok", "plan": plan}
    except Exception as e:
        logger.error("Fallback error: %s\n%s", e, traceback.format_exc())
        raise HTTPException(status_code=500, detail="Fallback generation failed.")

# Primary query endpoint
@app.post("/query")
async def query_travel_agent(request: QueryRequest = Body(...)):
    """
    Main endpoint used by Streamlit. 
    This tries to build and invoke the GraphBuilder agent (Groq) with retries and detailed logging.
    """
    try:
        logger.info("Received /query request (truncated): %s", (request.query[:200] + '...') if len(request.query) > 200 else request.query)

        # lazy import GraphBuilder to surface import errors in logs clearly
        try:
            from agent.agentic_workflow import GraphBuilder
        except Exception as e:
            logger.error("Could not import GraphBuilder from agent.agentic_workflow: %s\n%s", e, traceback.format_exc())
            raise HTTPException(status_code=500, detail="Server misconfiguration: GraphBuilder import failed. Check logs.")

        # create GraphBuilder with retries (transient network or auth errors may occur here)
        def build_graph():
            return GraphBuilder(model_provider='groq')

        try:
            graph_builder = retry_with_backoff(build_graph, max_attempts=3, base_delay=1.0, allowed_exceptions=(Exception,))
        except Exception as e:
            logger.error("Failed to construct GraphBuilder after retries: %s\n%s", e, traceback.format_exc())
            # upstream agent / API likely unavailable or keys invalid
            raise HTTPException(status_code=503, detail="Concierge / agent initialization failed. See server logs.")

        # call the graph builder to get the react_app (this may execute network calls depending on GraphBuilder impl)
        try:
            react_app = graph_builder()
        except Exception as e:
            logger.error("GraphBuilder() invocation failed: %s\n%s", e, traceback.format_exc())
            raise HTTPException(status_code=503, detail="Concierge / agent runtime failure. See server logs.")

        # optionally produce and save graph PNG if supported (wrap in try so failure here doesn't break the flow)
        try:
            if hasattr(react_app, "get_graph") and callable(getattr(react_app, "get_graph")):
                graph_obj = react_app.get_graph()
                if hasattr(graph_obj, "draw_mermaid_png"):
                    png_graph = graph_obj.draw_mermaid_png()
                    with open('my_graph.png', 'wb') as f:
                        f.write(png_graph)
                    logger.info("Graph saved as 'my_graph.png' in %s", os.getcwd())
        except Exception as e:
            # not fatal, only log
            logger.warning("Could not save graph PNG (non-fatal): %s\n%s", e, traceback.format_exc())

        # Prepare message payload - try the commonly used shapes; Graph agent may expect different one
        # We'll attempt multiple payload shapes so we are resilient to small contract mismatches.
        payload_variants = [
            {"messages": [{"role": "user", "content": request.query}]},  # common chat shape
            {"query": request.query},
            {"input": request.query},
            {"messages": [request.query]}  # your original version (keeps compatibility)
        ]

        def invoke_variant(payload):
            # this inner function should call react_app.invoke; wrap in try/except in outer retry
            return react_app.invoke(payload)

        last_exc = None
        for payload in payload_variants:
            try:
                logger.info("Trying payload variant: %s", list(payload.keys()))
                # retry the invoke a few times on transient errors
                result = retry_with_backoff(lambda: invoke_variant(payload), max_attempts=3, base_delay=1.0, allowed_exceptions=(Exception,))
                # success
                final_output = None
                # If result is dict, extract last message if present
                if isinstance(result, dict):
                    if "messages" in result:
                        try:
                            # handle message objects (.content) or plain dicts
                            last_msg = result["messages"][-1]
                            # if it's an object with .content
                            final_output = getattr(last_msg, "content", None) or (last_msg.get("content") if isinstance(last_msg, dict) else None)
                        except Exception:
                            logger.debug("Error extracting content from result['messages'], falling back to str(result).")
                    if not final_output and "answer" in result:
                        final_output = result["answer"]
                    if not final_output and "plan" in result:
                        final_output = result["plan"]
                if final_output is None:
                    # fallback to stringified result
                    final_output = str(result)
                return {"answer": final_output}
            except Exception as e:
                last_exc = e
                logger.warning("Payload variant failed: %s\n%s", payload.keys(), traceback.format_exc())
                # try next payload variant

        # If we reach here, all payload variants failed
        logger.error("All invoke payload variants failed. Last exception: %s\n%s", last_exc, traceback.format_exc())
        # return 503 to indicate temporary upstream/concierge failure so frontend can trigger fallback
        raise HTTPException(status_code=503, detail="Concierge service temporarily unavailable. All attempts failed.")

    except HTTPException:
        # re-raise to preserve status_code & details
        raise
    except Exception as e:
        # unexpected/unhandled errors - log full traceback
        logger.error("=== BACKEND /query ERROR START ===")
        logger.error("Unhandled exception: %s", e)
        logger.error(traceback.format_exc())
        logger.error("=== BACKEND /query ERROR END ===")
        raise HTTPException(status_code=500, detail="Internal server error - check server logs for details.")