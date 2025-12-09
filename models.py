from pydantic import BaseModel
from typing import List, Dict, Any, Optional

'''
Nodes are each node (each step of workflow) of graph, representing an uniqu identifier and 
tool name which is the function they will implement
id: string
toolname: string
'''
class Node(BaseModel):
    id: str
    tool_name: str

'''
Edges are each edge (each connection between nodes) of graph, representing source node, 
target node and a condition (opitional) to check if it branches bcz of some condition
source: string
target: string
condition: default is None
'''
class Edge(BaseModel):
    source: str
    target: str
    condition: Optional[str] = None

# Graph definition defines list of Nodes and Edges with start node for traversing
class GraphDefinition(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    start_node: str

# Wraps Graph inside Json
class WorkflowCreateRequest(BaseModel):
    graph: GraphDefinition

class WorkflowRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class WorkflowStatus(BaseModel):
    run_id: str
    status: str
    state: Dict[str, Any]
    logs: List[str]