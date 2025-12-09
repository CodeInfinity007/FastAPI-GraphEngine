import random
from .registry import registry

# Step 1
# Dummy function extracter from source code
@registry.register("extract_functions")
def extract_functions(state: dict):
    code = state.get("code", "")
    print(f"-> Extracting functions from code length {len(code)}")
    return {"functions": ["login_user", "process_payment", "send_email"]}


# Step 2
# Random Cyclometric complexity assignment to each func
@registry.register("check_complexity")
def check_complexity(state: dict):
    funcs = state.get("functions", [])
    score = state.get("complexity_score", random.randint(5, 15))
    
    # Code fixed simulation, reduce complexity by 5 everytime.
    # branches the workflow and loops till complexity is acceptable
    if state.get("loop_count", 0) > 0:
        score -= 5
        
    return {"complexity_score": score}

# Step 3
# Classifies Scores achieved into high or low complexity (ultimatly decied to loop again or not)
@registry.register("detect_issues")
def detect_issues(state: dict):
    score = state.get("complexity_score", 0)
    issues = []
    if score > 8:
        issues.append("Complexity too high")

    return {"issues": issues}

# Step 4
# Suggests Improvements based on comments recieved of issues list
@registry.register("suggest_improvements")
def suggest_improvements(state: dict):
    issues = state.get("issues", [])
    
    if "Complexity too high" in issues:
        loops = state.get("loop_count", 0) + 1
        return {
            "suggestion": "Refactor into smaller functions to reduce complexity",
            "loop_count": loops
        }
    
    return {"suggestion": "Code looks good"}