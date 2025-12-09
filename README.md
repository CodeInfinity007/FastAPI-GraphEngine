# FastAPI-GraphEngine

A lightweight, purely Python-based graph workflow engine built with FastAPI. It separates orchestration logic from business logic, allowing users to define dynamic workflows (DAGs) with conditional branching and loops via JSON.

## 📂 Project Structure

The project follows a modular architecture to separate concerns:

```text
/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI Entry Point & Background Tasks
│   ├── engine.py        # Core Graph Logic (State Machine & Traversal)
│   ├── models.py        # Pydantic Data Contracts (Input/Output Validation)
│   ├── registry.py      # Decorator-based Tool Registry
│   └── tools.py         # The "Code Review" Agent Implementation
└── README.md
```

## 🚀 How to Run

### 1. Install Dependencies


```
pip install fastapi uvicorn
```

### 2. Start the Server
```
uvicorn app.main:app --reload
```
Note: Run the application from the root directory

The server will start at `http://127.0.0.1:8000`.

Use at :  http://127.0.0.1:8000/docs


## ⚙️ Capabilities

This engine was designed to be **simple but architecture-aware**. It supports:

1.  **Dynamic Graph Definitions:** Workflows are not hardcoded. They are injected via JSON at runtime.
    
2.  **State Management:** A shared `state` dictionary flows through every node, accumulating data (State -> Transition -> Update).
    
3.  **Conditional Branching:** Edges support Python-expression conditions (e.g., `"score > 8"`) evaluated dynamically against the state.
    
4.  **Looping:** The engine supports cyclic graphs, allowing workflows to "retry" steps until a condition is met.
    
5.  **Tool Registry:** A decoupled system where Python functions are registered via decorators (`@registry.register`), keeping the engine agnostic of the specific business logic.
    

----------

## 🧪 Example Workflow: Code Review Agent

To test the engine, you can run the included "Code Review" workflow. This workflow simulates an agent that extracts code, checks complexity, and loops back to improve the code if quality is low.

### Step 1: Create the Graph

**POST** `/graph/create`

JSON

```
{
  "graph": {
    "nodes": [
      {"id": "step1", "tool_name": "extract_functions"},
      {"id": "step2", "tool_name": "check_complexity"},
      {"id": "step3", "tool_name": "detect_issues"},
      {"id": "step4", "tool_name": "suggest_improvements"}
    ],
    "edges": [
      {"source": "step1", "target": "step2"},
      {"source": "step2", "target": "step3"},
      {"source": "step3", "target": "step4", "condition": "complexity_score > 8"},
      {"source": "step4", "target": "step2", "condition": "loop_count < 2"}
    ],
    "start_node": "step1"
  }
}

```



### Step 2: Run the Workflow

**POST** `/graph/run`

JSON
```
{
  "graph_id": "<YOUR_GRAPH_ID_HERE>",
  "initial_state": {
    "code": "def complex_function(): # TODO: Fix me",
    "complexity_score": 12
  }
}

```



### Step 3: Check Status

**GET** `/graph/state/{run_id}`

You will see the state transition from having a high score (12) to a lower score as the loop executes.

----------

## 🔮 Future Improvements

If I had more time, I would address the following to make this production-ready:

1.  **Persistence:** Replace the in-memory `graphs_db` dictionary with a persistent database (PostgreSQL/SQLite) so workflows survive server restarts.
    
2.  **Security:** Replace `eval()` with a safe expression to prevent arbitrary code execution from JSON inputs.
    
3.  **Concurrency:** While `BackgroundTasks` works for this demo, I would implement a proper task queue for handling thousands of concurrent long-running workflows.
    
4.  **Observability:** Add structured logging and OpenTelemetry tracing to visualize the node traversal in real-time.