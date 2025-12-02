from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.save_to_document import save_document
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ✅ Root endpoint for GET and HEAD (for UptimeRobot)
@app.get("/")
@app.head("/")
def root():
    return JSONResponse(content={"status": "AI Trip Planner is running!", "version": "1.0"}, status_code=200)

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://roamio.streamlit.app'],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# ✅ Pydantic model
class QueryRequest(BaseModel):
    query: str

# ✅ Main POST endpoint
@app.post("/query")
async def query_travel_agent(request: QueryRequest):
    try:
        print(f"🔍 Received request: {request}")
        print(f"🔍 Query content: {request.query}")
        
        graph = GraphBuilder(model_provider='groq')
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open('my_graph.png', 'wb') as f:
            f.write(png_graph)
        print(f'Graph saved as \'my_graph.png\' in {os.getcwd()}')

        messages = {'messages': [request.query]}
        output = react_app.invoke(messages)

        if isinstance(output, dict) and 'messages' in output:
            final_output = output['messages'][-1].content
        else:
            final_output = str(output)

        return {'answer': final_output}

    except Exception as e:
        print(f"❌ Error details: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={'error': str(e)})