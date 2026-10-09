import os

os.environ["AZURE_OPENAI_API_KEY"] = "your-azure-openai-key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-azure-openai-resource-name.openai.azure.com/"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "gpt-4o"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-12-01-preview"
import json
from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# -------------------------------------------------------------------
# 1. Pydantic Schemas for Enforced Output Structures
# -------------------------------------------------------------------

class ResearchOutput(BaseModel):
    domain: str = Field(description="Industry or startup market domain")
    market_size_tam: str = Field(description="Estimated TAM/SAM/SOM market sizing breakdown")
    key_competitors: List[str] = Field(description="Top existing direct and indirect competitors")
    target_audience: str = Field(description="Ideal Customer Profile (ICP)")
    industry_trends: List[str] = Field(description="Key market drivers or emerging trends")

class FundingOutput(BaseModel):
    recommended_stage: str = Field(description="Recommended stage: e.g., Pre-Seed, Seed, Series A")
    target_raise: str = Field(description="Target raise capital amount")
    valuation_benchmark: str = Field(description="Estimated pre-money valuation range")
    monetization_model: str = Field(description="Primary monetization strategy")
    key_investor_metrics: List[str] = Field(description="Core KPIs investors will track")

class PitchDeckOutline(BaseModel):
    problem_statement: str = Field(description="Clear breakdown of customer pain points")
    solution: str = Field(description="Unique value proposition and solution product fit")
    market_opportunity: str = Field(description="Market sizing and opportunity narrative")
    business_model: str = Field(description="Unit economics and revenue strategy")
    go_to_market: str = Field(description="Acquisition and growth strategy")
    financials_and_ask: str = Field(description="Funding request with timeline and milestone goals")


# -------------------------------------------------------------------
# 2. Azure OpenAI Orchestration Engine
# -------------------------------------------------------------------

class AcceleratorWorkflowPlanner:
    def __init__(self):
        # Configure AzureChatOpenAI using environment variables
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

        self.llm = AzureChatOpenAI(
            azure_deployment=deployment_name,
            api_version=api_version,
            temperature=1.0
        )
        self.execution_trace: List[Dict[str, Any]] = []

    def _log_trace(self, agent_name: str, status: str, details: Any):
        """Captures intermediate agent steps and trace logs."""
        trace_entry = {
            "agent": agent_name,
            "status": status,
            "details": details
        }
        self.execution_trace.append(trace_entry)
        print(f"[{agent_name}] -> {status}")
        print(f"{json.dumps(details, indent=2) if isinstance(details, dict) else details}\n" + "-"*60)

    def research_agent(self, startup_domain: str, value_prop: str) -> ResearchOutput:
        """Agent 1: Deep-dives into market size, competition, and customer profiles."""
        parser = JsonOutputParser(pydantic_object=ResearchOutput)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Market Research Agent for a startup accelerator. Analyze the given industry domain and startup value proposition.\n{format_instructions}"),
            ("user", "Domain: {domain}\nValue Proposition: {value_prop}")
        ])

        chain = prompt | self.llm | parser

        self._log_trace("Research Agent", "EXECUTION_STARTED", {"domain": startup_domain})
        raw_result = chain.invoke({
            "domain": startup_domain,
            "value_prop": value_prop,
            "format_instructions": parser.get_format_instructions()
        })
        self._log_trace("Research Agent", "COMPLETED", raw_result)
        return ResearchOutput(**raw_result)

    def funding_advisor_agent(self, research_data: ResearchOutput) -> FundingOutput:
        """Agent 2: Formulates financial strategies and fundraising metrics based on research."""
        parser = JsonOutputParser(pydantic_object=FundingOutput)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Venture Capital Funding Advisor Agent. Provide financial modeling, valuation, and capital strategy recommendations based on market research.\n{format_instructions}"),
            ("user", "Research Context:\n{research_data}")
        ])

        chain = prompt | self.llm | parser

        self._log_trace("Funding Advisor Agent", "EXECUTION_STARTED", research_data.model_dump())
        raw_result = chain.invoke({
            "research_data": json.dumps(research_data.model_dump()),
            "format_instructions": parser.get_format_instructions()
        })
        self._log_trace("Funding Advisor Agent", "COMPLETED", raw_result)
        return FundingOutput(**raw_result)

    def pitch_coach_agent(self, research_data: ResearchOutput, funding_data: FundingOutput, feedback: str = None) -> PitchDeckOutline:
        """Agent 3: Combines outputs into a structured pitch deck outline with feedback loop capability."""
        parser = JsonOutputParser(pydantic_object=PitchDeckOutline)

        system_instruction = "You are a Pitch Deck Coach Agent. Synthesize research and funding recommendations into a 6-part pitch deck narrative structure.\n{format_instructions}"
        if feedback:
            system_instruction += f"\n\nCRITICAL REVIEW FEEDBACK (MUST FIX): {feedback}"

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            ("user", "Research Data:\n{research}\n\nFunding Strategy:\n{funding}")
        ])

        chain = prompt | self.llm | parser

        self._log_trace("Pitch Coach Agent", "EXECUTION_STARTED", {"feedback_loop_active": bool(feedback)})
        raw_result = chain.invoke({
            "research": json.dumps(research_data.model_dump()),
            "funding": json.dumps(funding_data.model_dump()),
            "format_instructions": parser.get_format_instructions()
        })
        self._log_trace("Pitch Coach Agent", "COMPLETED", raw_result)
        return PitchDeckOutline(**raw_result)

    def evaluate_quality(self, outline: PitchDeckOutline) -> Tuple[bool, str]:
        """Quality Gatekeeper: Validates output depth before final approval."""
        if len(outline.problem_statement) < 40:
            return False, "Problem statement is too brief. Expand on customer pain points."
        if len(outline.financials_and_ask) < 30:
            return False, "Financial ask lacks clear milestone allocation and funding targets."
        return True, "Passed quality checks."

    def run_pipeline(self, domain: str, value_prop: str) -> Dict[str, Any]:
        """Runs multi-agent pipeline with orchestrated logic and feedback loops."""
        print("============================================================")
        print("STARTING ACCELERATOR MULTI-AGENT WORKFLOW (AZURE OPENAI)")
        print("============================================================\n")

        # Step 1: Research Agent
        research = self.research_agent(domain, value_prop)

        # Step 2: Funding Advisor Agent
        funding = self.funding_advisor_agent(research)

        # Step 3: Pitch Coach Agent Initial Draft
        pitch_outline = self.pitch_coach_agent(research, funding)

        # Step 4: Quality Check & Feedback Loop Logic
        is_valid, feedback = self.evaluate_quality(pitch_outline)
        max_retries = 2
        retries = 0

        while not is_valid and retries < max_retries:
            retries += 1
            self._log_trace("Quality Reviewer", f"REJECTED (Attempt {retries})", f"Reason: {feedback}")
            pitch_outline = self.pitch_coach_agent(research, funding, feedback=feedback)
            is_valid, feedback = self.evaluate_quality(pitch_outline)

        if is_valid:
            self._log_trace("Quality Reviewer", "APPROVED", "Pitch deck outline passed verification.")

        return {
            "research": research.model_dump(),
            "funding": funding.model_dump(),
            "pitch_deck_outline": pitch_outline.model_dump(),
            "execution_trace": self.execution_trace
        }


# -------------------------------------------------------------------
# 3. Project Execution Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    planner = AcceleratorWorkflowPlanner()

    # Startup Sample Input
    sample_domain = "AI-Driven Logistics & Supply Chain Optimization"
    sample_value_prop = "Autonomous fleet routing and predictive warehouse demand forecasting using real-time IoT sensors."

    output = planner.run_pipeline(sample_domain, sample_value_prop)

    print("============================================================")
    print("FINAL DELIVERABLE: APPROVED PITCH DECK OUTLINE")
    print("============================================================")
    print(json.dumps(output["pitch_deck_outline"], indent=2))

    import json

# 1. Export the full output (including research, funding, pitch deck, and trace logs)
with open("accelerator_workflow_output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("Full workflow output successfully saved to 'accelerator_workflow_output.json'")

# 2. Export ONLY the final pitch deck outline
with open("pitch_deck_outline.json", "w", encoding="utf-8") as f:
    json.dump(output["pitch_deck_outline"], f, indent=4)

print("Pitch deck outline saved to 'pitch_deck_outline.json'")
