"""
app.py

Usage: python -m streamlit run app.py
"""

from pathlib import Path
from uuid import UUID

import streamlit as st

from agentml.agents import Agent, Coder, Vision
from agentml.manual import Manager


def can_retry(mngr: Manager) -> bool:
    """Check if the last agent can be retried"""

    if not st.session_state.get("messages"):
        return False

    _agent = mngr.last_run_agent
    if (
        _agent
        and isinstance(_agent, Agent)
        and (isinstance(_agent, Coder) or isinstance(_agent, Vision))
    ):
        return True
    return False


# Streamlit layout
st.set_page_config(layout="wide", page_icon="🤖")
st.title("AgentML")

left_column, right_column = st.columns(2, gap="large")

with left_column:
    with st.expander(
        "Initialize Manager", expanded=st.session_state.get("manager") is None
    ):
        # Input for initializing Manager
        goal = st.text_input("Enter the goal:", value="Build a classifier")
        csv_path = st.text_input("Enter the path to CSV file:", value="data/data.csv")
        session_id = st.text_input(
            "Enter the session ID:", value="11111111-1111-1111-1111-111111111111"
        )

        # Initialize the Manager
        init_manager_btn = st.button("Initialize Manager", use_container_width=True)
        if init_manager_btn:
            manager = Manager(
                goal=goal, csv=Path(csv_path), session_id=UUID(session_id)
            )
            st.session_state["manager"] = manager
            st.session_state[
                "messages"
            ] = []  # Initialize messages list in session state
            st.success(
                f"Manager initialized successfully with Session ID: {session_id}"
            )
            st.rerun()

    if "manager" in st.session_state:
        manager = st.session_state["manager"]
        st.divider()

        st.subheader("Tasks")
        for task in manager.tasks:
            for agent, objective in task.items():
                st.write(f"`{agent.__name__}` {objective}")

        with st.expander("Add Task"):
            add_task_agent = st.selectbox("Agent", ("Coder", "Planner", "Vision"))
            add_task_objective = st.text_input("Objective", key="new_task_objective")

            def add_task():
                """Add a task to the manager"""
                if add_task_objective:
                    manager.add_task({add_task_agent: add_task_objective})
                    st.session_state["new_task_objective"] = ""

            add_task_btn = st.button(
                "Add Task", on_click=add_task, use_container_width=True
            )

        with st.expander("Delete Task"):
            if manager.tasks:
                task_options = [
                    f"{agent.__name__}: {objective}"
                    for task in manager.tasks
                    for agent, objective in task.items()
                ]
                selected_task_index = st.selectbox(
                    "Select a task to delete",
                    range(len(task_options)),
                    format_func=lambda x: task_options[x],
                )

                delete_task_btn = st.button("Delete Task", use_container_width=True)
                if delete_task_btn:
                    manager.delete_task(idx=selected_task_index)
                    st.rerun()

        st.divider()

        task_btn_col, run_btn_col = st.columns(2)

        with task_btn_col:
            get_task_btn = st.button(
                "Get Task",
                use_container_width=True,
                help="Preview the next task in the queue.",
            )

        with run_btn_col:
            run_agent_btn = st.button(
                "Run Agent",
                disabled=not manager.tasks,
                use_container_width=True,
                help="Run the next agent in the queue.",
            )

        if get_task_btn and manager.tasks:
            task = manager.tasks[0]
            for agent, objective in task.items():
                st.write(f"`{agent.__name__}`: {objective}")

        if run_agent_btn:
            with st.spinner("Running Agent..."):
                st.session_state["messages"] = manager.run()

        st.subheader("Messages")
        for index, msg in enumerate(st.session_state.get("messages", [])):
            st.chat_message(msg.role.value).write(msg.content)

        with st.expander("Update Messages", expanded=False):
            for index, msg in enumerate(st.session_state.get("messages", [])):
                key = f"msg_{index}"
                updated_message = st.text_input(
                    f"Update {msg.role.value} message:", value=msg.content, key=key
                )
                st.session_state["messages"][
                    index
                ].content = updated_message  # Update the message content

        retry_btn_col, validate_btn_col = st.columns(2)

        with validate_btn_col:
            validate_run_btn = st.button(
                "Validate",
                disabled=not st.session_state.get("messages"),
                use_container_width=True,
                help="Approve the run and move on to the next task.",
            )
            if validate_run_btn:
                with st.spinner("Validating..."):
                    manager.validate_run(st.session_state["messages"])
                    st.success("Validation completed.")
                    st.session_state["messages"] = []
                    st.rerun()

        with retry_btn_col:
            retry_btn = st.button(
                "Retry",
                disabled=not can_retry(manager),
                use_container_width=True,
                help="Retry the last agent (only works for Coder and Vision).",
            )
            if retry_btn:
                with st.spinner("Retrying..."):
                    st.session_state["messages"] = manager.retry_last_agent()
                    st.success("Retry completed.")
                    st.rerun()

with right_column:
    st.header("Agent Log")
    log_refresh_btn = st.button("Refresh Log", use_container_width=True)
    if log_refresh_btn:
        st.rerun()

    if "manager" in st.session_state:
        manager = st.session_state["manager"]

        for msg in manager.messages:
            st.chat_message(msg.role.value).write(msg.content)
