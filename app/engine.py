from uuid import uuid4
from collections import defaultdict
from .models import WorkflowStatus
from .registry import registry

runs_db = {}

class WorkflowEngine:
    def __init__(self, graph_def, initial_state):
        self.graph_def = graph_def
        self.state = initial_state
        self.run_id = str(uuid4())
        self.status = "pending"

        # Map ID to Node for O(1) lookup
        self.node_map = {}
        for n in graph_def.nodes:
            self.node_map[n.id] = n
        
        # Adjacency List
        self.adj_list = defaultdict(list)
        for edge in graph_def.edges:
            self.adj_list[edge.source].append(edge)

    def run(self):
        self.status = "running"
        runs_db[self.run_id] = self
        
        current_id = self.graph_def.start_node

        try:
            while current_id:
                node = self.node_map.get(current_id)
                tool_func = registry.get_tool(node.tool_name)
                result = tool_func(self.state)
                if result:
                    self.state.update(result)

                next_id = None
                for edge in self.adj_list[current_id]:
                    # eval used here for demonstrative purposes, not to be used in prod due to code injection risk
                    if not edge.condition or eval(edge.condition, {}, self.state):
                        next_id = edge.target
                        break
                
                current_id = next_id
            
            self.status = "completed"

        except Exception as e:
            self.status = "failed"

    def get_status(self):
        return WorkflowStatus(
            run_id=self.run_id,
            status=self.status,
            state=self.state,
        )