from fastapi import FastAPI, HTTPException, BackgroundTasks
from uuid import uuid4
from .models import WorkflowCreateRequest, WorkflowRunRequest, WorkflowStatus
from .engine import WorkflowEngine, runs_db
from . import tools 

app = FastAPI(title="Graph Engine")

graphs_db = {}

@app.post("/graph/create")
def create_graph(request: WorkflowCreateRequest):
    graph_id = str(uuid4())
    graphs_db[graph_id] = request.graph
    return {"graph_id": graph_id, "message": "Graph saved."}

@app.post("/graph/run")
def run_graph(request: WorkflowRunRequest, background_tasks: BackgroundTasks):
    graph_def = graphs_db.get(request.graph_id)
    if not graph_def:
        raise HTTPException(status_code=404, detail="Graph ID not found")
    
    engine = WorkflowEngine(graph_def, request.initial_state)
    

    background_tasks.add_task(engine.run)
    
    return {
        "run_id": engine.run_id,
        "status": "started",
        "check_status_url": f"/graph/state/{engine.run_id}"
    }

@app.get("/graph/state/{run_id}", response_model=WorkflowStatus)
def get_state(run_id: str):
    engine = runs_db.get(run_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return engine.get_status()