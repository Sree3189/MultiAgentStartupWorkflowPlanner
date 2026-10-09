# Multi-Agent Workflow Planner for Startup Accelerator (Azure OpenAI)

## Overview
This project delivers an orchestrated multi-agent planning workflow designed for startup accelerators. Using specialized agents and Azure OpenAI, the workflow generates market research, financial/fundraising metrics, and structured pitch deck outlines for early-stage startup founders.

## Architecture
- **Research Agent**: Collects domain data, TAM estimates, competitor breakdowns, and ICP profiles.
- **Funding Advisor Agent**: Recommends appropriate funding rounds, valuation benchmarks, and KPIs.
- **Pitch Coach Agent**: Converts insights into a 6-slide narrative outline.
- **Quality Feedback Loop**: Evaluates output completeness and forces re-evaluation if criteria are not met.

## Prerequisites
- Python 3.10 or higher
- Access to an Azure OpenAI deployment (e.g., `gpt-5-mini`)

## Environment Variables
Ensure the following variables are exported:
```bash
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="[https://your-resource-name.openai.azure.com/](https://your-resource-name.openai.azure.com/)"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-5-mini"
export AZURE_OPENAI_API_VERSION="2024-04-01-preview"

### Steps to Run and Inspect Project Results

1. **Terminal Setup**: Open your terminal or IDE (VS Code, PyCharm).
2. **Export Environment Variables**: Set your Azure OpenAI Endpoint and Key as described in Step 2.
3. **Run Code**: Execute `python app.py`.
4. **Observe Results**:
   * Inspect the real-time execution logs starting with `[Research Agent] -> EXECUTION_STARTED` to trace the data flow through each agent.
   * Verify the `[Quality Reviewer]` approval step.
   * View the final generated JSON structure printed under `FINAL DELIVERABLE: APPROVED PITCH DECK OUTLINE`.
