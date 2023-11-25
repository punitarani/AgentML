# AgentML

**AgentML is a groundbreaking LLM Agent tool designed to revolutionize the machine learning (ML) landscape.**

Offering simplicity and power, it's suited for a diverse audience, from students to ML professionals and non-coders.
AgentML streamlines ML processes for all types of datasets, embodying innovation in artificial intelligence.

## Demo

The following demo videos showcase AgentML's capabilities in both Supervised and Autonomous modes.

AgentML is capable of handling datasets, writing code and also training and evaluating machine learning models.

![AgentML Highlight](docs/training-demo.png)

### Supervised Mode Video

Human-in-the-loop mode to train a classifier on the Iris dataset.

[![AgentML Supervised Demo](docs/tasks-demo.png)](https://drive.google.com/file/d/1FmeKT7AlslZPFocpZgVqKc1bzUgE2rAn/view?usp=sharing)

### Autonomous Mode Video

Autonomous mode with validator pseudo-agent to replace human validation.

[![AgentML Autonomous Demo](docs/autonomous-demo.png)](https://drive.google.com/file/d/19BLRT-t8P0pI8lcz8q3kvFDCQcS51Akz/view?usp=sharing)

> Video is sped up for brevity.

## Key Features

### Dual Capability in ML Workflow

- **Small Datasets:**
    - **Data Analysis:** Analyzes dataset characteristics to grasp the problem statement.
    - **Pipeline Creation:** Develops a comprehensive pipeline, including data preprocessing, model building, and
      evaluation.
    - **Iterative Refinement:** Continuously refines the model for optimal performance.
- **Complex Datasets:**
    - **Advanced Data Handling:** Manages intricate datasets with enhanced preprocessing and analysis.
    - **Custom Model Building:** Constructs tailored models to address complex problems.
    - **In-depth Evaluation:** Provides thorough model evaluation and tuning for complex datasets.

### User Interaction and Customization

- **Code Execution:**
    - **Secure Environment:** Executes Python code in a sandbox for safety and integrity.
    - **Interactive Development:** Allows real-time code writing and testing.
- **Template Utilization:**
    - **Customizability:** Imports and builds on user-provided code templates.
    - **Flexibility:** Adapts to various coding styles and requirements.

### Vision Agent

- **Advanced Data Interpretation:**
    - **Visual Data Analysis:** Interprets charts and graphs for deeper insights.
    - **Enhanced Perception:** Supplements language models with visual understanding.

## Technical Architecture

### Manager Agent

- **Role:**
    - **Central Coordination:** Manages inputs and oversees other agents' operations.
    - **Goal-Oriented Management:** Focuses on achieving user-defined goals.
- **Function:**
    - **Integration:** Ensures cohesive operation of all agents.
    - **Efficiency:** Optimizes resource allocation and task execution.

### Planner Agent

- **Responsibility:**
    - **Task Analysis:** Breaks down goals into manageable tasks.
    - **Efficient Delegation:** Allocates tasks to the appropriate agents.
- **Strategic Planning:**
    - **Methodical Approach:** Ensures systematic problem-solving.
    - **Goal Alignment:** Aligns tasks with the overarching objectives.

### Coder Agent

- **Capabilities:**
    - **Diverse Coding Tasks:** Handles writing, modifying, and debugging code.
    - **Model Development:** Builds and visualizes ML models.
- **Automation:**
    - **Recursive Execution:** Ensures thorough and accurate completion of coding tasks.
    - **Error Handling:** Detects and resolves errors in code to ensure smooth execution.

### Vision Agent

- **Functionality:**
    - **Data Visualization Analysis:** Interprets visual data for comprehensive insights.
    - **Cross-Model Integration:** Combines visual analysis with other model outputs.

### Validator (Pseudo-Agent)

- **In Autonomous Mode** (LLM Agent):
    - **Step Validation:** Checks each step for alignment with goals.
    - **Consistency Assurance:** Ensures uniformity in autonomous operations.
- **In Supervised Mode** (Human-in-the-loop):
    - **User Oversight:** Allows users to guide and validate the process.
    - **Customization and Control:** Enables user-driven adjustments and decision-making.

## User Accessibility and Interface

- **User-Friendly Design:**
    - **Ease of Use:** Intuitive interface for a wide range of users.
    - **Guided Interaction:** Simplifies ML concepts for easy understanding.
- **Inclusivity:**
    - **Non-Coder Friendly:** Accessible to individuals without coding background.
    - **Professional Versatility:** Meets the needs of experienced ML practitioners.

## Web Application for Deployment

- **Easy Access:**
    - **Simple Interface:** Streamlined web app for easy AgentML deployment.
    - **Instant Setup:** Quick start-up with minimal configuration.
- **Broad Accessibility:**
    - **Universal Reach:** Available to a global audience.
    - **No Expertise Required:** User-friendly for all skill levels.

AgentML is more than a tool—it's a transformative force in machine learning, offering ease, efficiency, and advanced
insights. It exemplifies the democratizing power of artificial intelligence, making sophisticated ML processes
accessible to everyone.

## Running the Application

AgentML can be operated in two modes: Supervised and Autonomous. Follow these simple steps to get started:

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

### Supervised Mode

```bash
python -m streamlit run app.py
```

### Autonomous Mode

```bash
python -m streamlit run auto.py
```

---

Punit Arani
