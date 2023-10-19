# AgentML

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting Up the Development Environment](#setting-up-the-development-environment)
- [Code Formatting and Linting](#code-formatting-and-linting)

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/) (recommended; or newer)
- [Poetry](https://python-poetry.org/docs/) for dependency management.

## Setting Up the Development Environment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/punitarani/AgentML.git
   cd AgentML
   ```

2. **Install Dependencies using Poetry**:

   ```bash
   poetry install
   ```

   Poetry should automatically create a virtual environment for you.
   If it doesn't, you can initiate one manually:

   ```bash
   poetry shell
   ```

3. **Setup Environment Variables**:
    - Copy the `.config/.env.template` to `.env` in the root directory.
    - Fill out the necessary environment variables in the `.env` file.

4. **Setup Pre-commit Hooks**:
   Use the provided Makefile to set up the necessary pre-commit hooks:

   ```bash
    make setup
    ```

## Code Formatting and Linting

- **Format Code**:
   ```bash
   make format
   ```
- **Lint Code**:
   ```bash
   make lint
   ```
