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
