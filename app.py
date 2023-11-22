"""
app.py

Usage: python -m streamlit run app.py
"""

from pathlib import Path
from uuid import UUID

import streamlit as st

from agentml import Manager
from agentml.agents import Coder, Planner, Vision

# Streamlit layout
st.set_page_config(layout="wide", page_icon="🤖")
st.title("Agent Manager Interface")

# Input for initializing Manager
goal = st.text_input("Enter the goal:", value="Build a classifier")
csv_path = st.text_input("Enter the path to CSV file:", value="data/data.csv")
session_id = st.text_input(
    "Enter the session ID:", value="11111111-1111-1111-1111-111111111111"
)

# Initialize Manager
if st.button("Initialize Manager"):
    if not Path(csv_path).exists():
        st.error("CSV file does not exist.")
    else:
        session_id = UUID(session_id) if session_id else UUID()
        manager = Manager(goal, Path(csv_path), session_id)
        st.session_state["manager"] = manager
        st.success(f"Manager initialized with session ID: {session_id}")


# Function to convert task string to dictionary
def parse_task(task_str):
    agent_str, objective = task_str.split(": ", 1)
    agent_class = {"Planner": Planner, "Coder": Coder, "Vision": Vision}.get(agent_str)
    if not agent_class:
        raise ValueError(f"Invalid agent type: {agent_str}")
    return {agent_class: objective}


# Task Queue Management
if "manager" in st.session_state:
    manager = st.session_state["manager"]
    st.header("Task Queue")
    task_list = st.text_area(
        "Edit tasks (Agent: Objective)",
        value="\n".join(
            [
                f"{agent.__name__}: {objective}"
                for task in manager.tasks
                for agent, objective in task.items()
            ]
        ),
    )

    if st.button("Update Tasks"):
        # Parse and update tasks
        tasks = [
            parse_task(task_str)
            for task_str in task_list.split("\n")
            if task_str.strip()
        ]
        manager.tasks = tasks
        st.success("Tasks updated.")

    # Execute Tasks
    st.header("Execute Tasks")
    if st.button("Run Next Task"):
        if manager.tasks:
            task = manager.tasks.pop(0)
            output = manager.run_single_task(task)
            st.write("Task Output:", output)
        else:
            st.warning("No more tasks in the queue.")
