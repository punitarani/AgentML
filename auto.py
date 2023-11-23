"""
app.py

Usage: python -m streamlit run auto.py
"""

from pathlib import Path
from uuid import UUID, uuid4

import streamlit as st

from agentml.manual import Manager
from agentml.models import LlmRole

# Streamlit layout for the automated page
st.set_page_config(layout="wide", page_icon="🤖")
st.title("Auto AgentML")

# Initialize Manager
with st.expander(
    "Initialize Manager", expanded=st.session_state.get("manager") is None
):
    # Input for initializing Manager
    goal = st.text_input("Enter the goal:", value="Build a classifier")
    csv_path = st.text_input("Enter the path to CSV file:", value="data/data.csv")
    session_id = st.text_input("Enter the session ID:", value=str(uuid4()))

    # Initialize the Manager
    init_manager_btn = st.button("Initialize Manager", use_container_width=True)
    if init_manager_btn:
        with st.spinner("Initializing Manager..."):
            manager = Manager(
                goal=goal, csv=Path(csv_path), session_id=UUID(session_id)
            )
            st.session_state["manager"] = manager
            st.session_state["messages"] = []
        st.success(f"Manager initialized successfully with Session ID: {session_id}")
        st.rerun()

if "manager" in st.session_state:
    manager = st.session_state["manager"]

    while manager.tasks:
        # Get the current task information
        current_task = manager.tasks[
            0
        ]  # Assuming the current task is at the top of the queue
        task_info = f"{', '.join(f'`{agent.__name__}`: {objective}' for agent, objective in current_task.items())}"

        with st.spinner(task_info):
            # Automatically run the next agent
            output = manager.run()

            # Automatically decide to retry or validate based on the output
            last_output = output[-1]
            last_content = (
                last_output.content if last_output.role == LlmRole.ASSISTANT else ""
            )
            decision = manager.next(last_content)
            if decision == "retry":
                with st.spinner("Retrying the last agent..."):
                    manager.retry_last_agent()
            elif decision == "validate":
                manager.validate_run(output)

        # Display the output for the current task in chat format
        for msg in output:
            st.chat_message(msg.role.value).write(msg.content)

        # Check and break the loop if no more tasks are available
        if not manager.tasks:
            done = manager.done(last_content)
            if done:
                st.success("All tasks completed.")
                break

            # Call planner to generate new tasks
            manager.tasks = [
                {"Planner": "Continue to generate the next steps to achieve the goal"}
            ]

    st.subheader("Tasks")
    for task in manager.tasks:
        for agent, objective in task.items():
            st.write(f"`{agent.__name__}` {objective}")
