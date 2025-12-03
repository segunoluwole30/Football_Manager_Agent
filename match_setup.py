from strategy_reasoning import generate_tactic_plan
from apply_tactics import apply_tactic_plan

def main():
    plan = generate_tactic_plan()
    print("LLM chose:", plan)
    apply_tactic_plan(plan)

if __name__ == "__main__":
    main()
