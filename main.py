from graph import app
from langchain_core.messages import HumanMessage
import uuid

# 1. Ask the user for a topic
print("\n" + "═"*30)
user_topic = input("🧬 Enter a research topic: ")
print("═"*30 + "\n")

# 2. Generate a unique thread ID for this session
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

# 3. Prepare inputs
inputs = {
    "query": user_topic,
    "messages": [HumanMessage(content=user_topic)],
    "revision_count": 0,
    "is_satisfactory": False
}

print(f"🚀 Swarm is analyzing: {user_topic}...")

# 4. Stream the output (This looks great in recordings!)
for event in app.stream(inputs, config=config):
    for node, value in event.items():
        print(f"\n📍 Node '{node}' is finished.")

# 5. Get the final result
final_state = app.get_state(config)
messages = final_state.values["messages"]

print("\n" + "█"*60)
print("🎯 FINAL AGENTIC REPORT")
print("█"*60)

# Display the final finding
for msg in reversed(messages):
    if "Findings:" in msg.content:
        print(msg.content)
        break

print("\n" + "█"*60)