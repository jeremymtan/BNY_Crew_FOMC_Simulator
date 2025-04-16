from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource


from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource


from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai import LLM
import os

### Add knowledge sources individually
date = "24_3"

# Individual PDF knowledge sources
beige_book_source = PDFKnowledgeSource(file_paths=[f"{date} beige book.pdf"])
current_macro_source: PDFKnowledgeSource = PDFKnowledgeSource(file_paths=[f"{date} current macro 1.pdf"])
dot_plot_source = PDFKnowledgeSource(file_paths=[f"{date} dot plot description.pdf"])
fed_explanation_source: PDFKnowledgeSource = PDFKnowledgeSource(file_paths=["Fed Explanation.pdf"])

# CSV knowledge source
historical_macro_source = CSVKnowledgeSource(file_paths=[f"{date} historical macro.csv"])

### add llm
managerllm = LLM(model="openai/gpt-4o", temperature=0.03)
# Always keep manager as GPT 4o

gpt_llm = LLM(model="openai/gpt-4o-mini", temperature=0.03)

# deepseek_llm = LLM(
#     model="openrouter/deepseek/deepseek-r1",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.environ["OPENROUTER_API_KEY"],
# )

# claude_llm = LLM(
#     model="claude-3-5-sonnet-20240620",
#     base_url="https://api.anthropic.com",
#     api_key=os.environ["ANTHROPIC_API_KEY"],
# )


@CrewBase
class BnyCapstoneCrew:
    """FOMC Simulation crew with Chain of Draft and sequential knowledge source processing"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Define agents with empty knowledge sources - we'll add them in specific tasks
    @agent
    def economist(self) -> Agent:
        return Agent(
            config=self.agents_config["economist"],
            verbose=True,
            llm="gpt-4o",
            max_iter=50,
        )

    @agent
    def Regional_Pragmatists(self) -> Agent:
        return Agent(
            config=self.agents_config["Regional_Pragmatists"],
            verbose=True,
            llm=gpt_llm,
            max_iter=50,
            memory=True,
        )

    @agent
    def Academic_Balancers(self) -> Agent:
        return Agent(
            config=self.agents_config["Academic_Balancers"],
            verbose=True,
            llm=gpt_llm,
            max_iter=50,
            memory=True,
        )

    @agent
    def Central_Policymakers(self) -> Agent:
        return Agent(
            config=self.agents_config["Central_Policymakers"],
            verbose=True,
            llm=gpt_llm,
            max_iter=50,
            memory=True,
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst"],
            verbose=True,
            llm=gpt_llm,
            max_iter=50,
            memory=True,
        )

    # Individual knowledge source analysis tasks
    @task 
    def analyze_current_macro(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze current macro data with minimal steps, 30 words max per step.
            
            Examine the current macro 1.pdf file only.
            Focus on:
            1. Key economic indicators
            2. Recent trends
            3. Implied probabilities from CME Fedwatch
            
            Format as:
            "Indicator: value; trend; implication"
            "Probability: scenario; percentage; meaning"
            
            Return analysis after "####".
            """,
            agent=self.economist(),
            knowledge_source=current_macro_source,
            expected_output="Concise, draft-style analysis of current macro data.",
        )
    
    @task 
    def analyze_historical_macro(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze historical macro data with minimal steps, 30 words max per step.
            
            Examine the historical macro data only.
            Focus on:
            1. Long-term trends
            2. Historical patterns
            3. Comparative contexts
            
            Format as:
            "Trend: metric; direction; timeframe"
            "Pattern: period; behavior; significance"
            "Comparison: current vs. historical; implication"
            
            Return analysis after "####".
            """,
            agent=self.economist(),
            knowledge_source=historical_macro_source,
            expected_output="Concise, draft-style analysis of historical macro data.",
        )

    @task 
    def regional_beige_book_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze Beige Book with minimal steps, 30 words max per step.
            
            As Regional Pragmatists, examine the Beige Book only.
            Focus on:
            1. Regional economic conditions
            2. Business activity patterns
            3. Labor markets
            4. Inflation pressures
            
            Format as:
            "Region: condition; trend; outlook"
            "Sector: activity; challenges; opportunities"
            "Labor: tightness; wages; hiring"
            "Prices: level; direction; drivers"
            
            Return analysis after "####".
            """,
            agent=self.Regional_Pragmatists(),
            knowledge_source=beige_book_source,
            expected_output="Concise, draft-style analysis of Beige Book from regional perspective.",
        )
    
    @task 
    def regional_current_macro_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze current macro with minimal steps, 30 words max per step.
            
            As Regional Pragmatists, examine the current macro 1.pdf only.
            Focus on:
            1. Regional implications
            2. Market expectations
            3. Near-term regional forecasts
            
            Format as:
            "Indicator: value; regional impact"
            "Market: expectation; regional significance"
            "Forecast: scenario; regional outcome"
            
            Return analysis after "####".
            """,
            agent=self.Regional_Pragmatists(),
            knowledge_source=current_macro_source,
            expected_output="Concise, draft-style analysis of current macro from regional perspective.",
        )
    
    @task 
    def regional_historical_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze historical data with minimal steps, 30 words max per step.
            
            As Regional Pragmatists, examine historical macro data only.
            Focus on:
            1. Regional historical patterns
            2. Previous policy cycles
            3. Regional economic responses
            
            Format as:
            "Historical period: date; regional impact"
            "Policy cycle: timing; regional effect"
            "Response pattern: situation; regional outcome"
            
            Return analysis after "####".
            """,
            agent=self.Regional_Pragmatists(),
            knowledge_source=historical_macro_source,
            expected_output="Concise, draft-style analysis of historical data from regional perspective.",
        )
    
    @task 
    def academic_dot_plot_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze dot plot with minimal steps, 30 words max per step.
            
            As Academic Balancers, examine dot plot description only.
            Focus on:
            1. Rate projections
            2. Committee dispersion
            3. Forward guidance implications
            
            Format as:
            "Projection: timeframe; central tendency"
            "Dispersion: range; meaning; significance"
            "Guidance: signal; theoretical implication"
            
            Return analysis after "####".
            """,
            agent=self.Academic_Balancers(),
            knowledge_source=dot_plot_source,
            expected_output="Concise, draft-style analysis of dot plot from academic perspective.",
        )
    
    @task 
    def academic_current_macro_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze current macro with minimal steps, 30 words max per step.
            
            As Academic Balancers, examine current macro 1.pdf only.
            Focus on:
            1. Theoretical implications
            2. Model consistency
            3. Equilibrium indicators
            
            Format as:
            "Theory: evidence; consistency; deviation"
            "Model: prediction; actual; adjustment"
            "Equilibrium: indicator; status; direction"
            
            Return analysis after "####".
            """,
            agent=self.Academic_Balancers(),
            knowledge_source=current_macro_source,
            expected_output="Concise, draft-style analysis of current macro from academic perspective.",
        )
    
    @task 
    def academic_historical_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze historical data with minimal steps, 30 words max per step.
            
            As Academic Balancers, examine historical macro data only.
            Focus on:
            1. Economic theory validation
            2. Long-term equilibrium patterns
            3. Policy effectiveness metrics
            
            Format as:
            "Theory: principle; historical evidence"
            "Equilibrium: measure; historical pattern"
            "Policy: action; effectiveness; timing"
            
            Return analysis after "####".
            """,
            agent=self.Academic_Balancers(),
            knowledge_source=historical_macro_source,
            expected_output="Concise, draft-style analysis of historical data from academic perspective.",
        )
    
    @task 
    def central_fed_explanation_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze Fed Explanation with minimal steps, 30 words max per step.
            
            As Central Policymakers, examine Fed Explanation only.
            Focus on:
            1. Policy framework principles
            2. Communication strategy
            3. Institutional considerations
            
            Format as:
            "Framework: principle; application; importance"
            "Communication: strategy; effectiveness; improvement"
            "Institution: consideration; constraint; opportunity"
            
            Return analysis after "####".
            """,
            agent=self.Central_Policymakers(),
            knowledge_source=fed_explanation_source,
            expected_output="Concise, draft-style analysis of Fed Explanation from central perspective.",
        )
    
    @task 
    def central_current_macro_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze current macro with minimal steps, 30 words max per step.
            
            As Central Policymakers, examine current macro 1.pdf only.
            Focus on:
            1. Policy stance implications
            2. Financial stability considerations
            3. Market communication aspects
            
            Format as:
            "Policy: indicator; implication; adjustment"
            "Stability: risk; assessment; response"
            "Communication: signal; market reaction; adjustment"
            
            Return analysis after "####".
            """,
            agent=self.Central_Policymakers(),
            knowledge_source=current_macro_source,
            expected_output="Concise, draft-style analysis of current macro from central perspective.",
        )
    
    @task 
    def central_historical_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze historical data with minimal steps, 30 words max per step.
            
            As Central Policymakers, examine historical macro data only.
            Focus on:
            1. Policy precedents
            2. Institutional memory
            3. Long-term policy effectiveness
            
            Format as:
            "Precedent: situation; action; outcome"
            "Memory: event; lesson; application"
            "Effectiveness: policy; result; timeframe"
            
            Return analysis after "####".
            """,
            agent=self.Central_Policymakers(),
            knowledge_source=historical_macro_source,
            expected_output="Concise, draft-style analysis of historical data from central perspective.",
        )

    # Define economist tasks with Chain of Draft
    @task
    def probabilities_comment(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Comment on implied probabilities in current macro 1.pdf.
            Keep steps minimal, 5 words max per step.
            Format notes as "key point: data".
            Return final points after "####".
            
            Explain what this means. Data from CME Fedwatch website.
            """,
            agent=self.analyst(),
            knowledge_source=current_macro_source,
            expected_output="Concise, draft-style comment on implied probabilities from current macro 1.pdf, explaining meaning in minimal steps.",
        )

    @task
    def get_economic_suggestions(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Propose monetary policy options, 30 words max per step.
            
            Based on your analysis of:
            - Current macro data
            - Historical macro data
            - Market-implied probabilities
            
            Propose 3 monetary policy solutions, each with:
            1. Title with specific numerical rate adjustment
            2. Justification (economic data)
            3. Projected outcomes
            4. Reference to implied probabilities
            
            Format as "Solution #: rate change; justification; outcomes"
            
            No preliminary leanings/advice. Number solutions clearly.
            Never propose options with 0% implied probability.
            
            Return solutions after "####".
            """,
            agent=self.economist(),
            context=[
                self.analyze_current_macro(),
                self.analyze_historical_macro(),
                self.probabilities_comment()
            ],
            expected_output="Concise, draft-style monetary policy options following Chain of Draft format.",
        )

    # Consolidated analysis tasks with Chain of Draft
    @task
    def regional_consolidated_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze economist proposals with minimal steps, 30 words max per step.
            
            As Regional Pragmatists, combine your analyses of:
            - Beige Book
            - Current macro data
            - Historical data
            
            Evaluate each proposed solution considering:
            1. Regional economic impacts
            2. Dual mandate alignment
            3. Historical comparisons (exact dates)
            4. Prediction for 2025 year-end Fed Funds rate
            
            Format as:
            "Solution #: strength; weakness; regional impact"
            "Historical comparison: date; similarity; outcome"
            "Regional indicators: metric; trend; implication"
            "Leaning: solution; rationale; regional benefit"
            "2025 prediction: rate; reasoning"
            
            Return analysis after "####".
            """,
            agent=self.Regional_Pragmatists(),
            context=[
                self.regional_beige_book_analysis(),
                self.regional_current_macro_analysis(),
                self.regional_historical_analysis(),
                self.get_economic_suggestions(),
                self.probabilities_comment()
            ],
            expected_output="Concise, draft-style consolidated analysis from Regional Pragmatists.",
        )

    @task
    def academic_consolidated_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze economist proposals with minimal steps, 30 words max per step.
            
            As Academic Balancers, combine your analyses of:
            - Dot plot description
            - Current macro data
            - Historical data
            
            Evaluate each proposed solution considering:
            1. Theoretical consistency
            2. Dual mandate alignment
            3. Historical comparisons (exact dates)
            4. Prediction for 2025 year-end Fed Funds rate
            
            Format as:
            "Solution #: strength; weakness; theoretical alignment"
            "Historical comparison: date; similarity; outcome"
            "Academic indicators: metric; trend; implication"
            "Leaning: solution; rationale; theoretical basis"
            "2025 prediction: rate; reasoning"
            
            Return analysis after "####".
            """,
            agent=self.Academic_Balancers(),
            context=[
                self.academic_dot_plot_analysis(),
                self.academic_current_macro_analysis(),
                self.academic_historical_analysis(),
                self.get_economic_suggestions(),
                self.probabilities_comment()
            ],
            expected_output="Concise, draft-style consolidated analysis from Academic Balancers.",
        )

    @task
    def central_consolidated_analysis(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Analyze economist proposals with minimal steps, 30 words max per step.
            
            As Central Policymakers, combine your analyses of:
            - Fed Explanation
            - Current macro data
            - Historical data
            
            Evaluate each proposed solution considering:
            1. Policy framework alignment
            2. Dual mandate balance
            3. Historical comparisons (exact dates)
            4. Prediction for 2025 year-end Fed Funds rate
            
            Format as:
            "Solution #: strength; weakness; policy alignment"
            "Historical comparison: date; similarity; outcome"
            "Policy indicators: metric; trend; implication"
            "Leaning: solution; rationale; policy basis"
            "2025 prediction: rate; reasoning"
            
            Return analysis after "####".
            """,
            agent=self.Central_Policymakers(),
            context=[
                self.central_fed_explanation_analysis(),
                self.central_current_macro_analysis(),
                self.central_historical_analysis(),
                self.get_economic_suggestions(),
                self.probabilities_comment()
            ],
            expected_output="Concise, draft-style consolidated analysis from Central Policymakers.",
        )

    # Define individual discussion tasks with Chain of Draft
    @task
    def regional_discussion(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Respond to analyses with minimal steps, 30 words max per step.
            
            As Regional Pragmatists:
            1. Address key points from others
            2. Defend/clarify your position
            3. Note any mind changing
            4. Highlight regional considerations
            
            Format as:
            "Member point: agreement/disagreement; reason"
            "Position clarification: point; rationale"
            "Regional factors: indicator; implication"
            "Updated leaning: solution; reason"
            "Updated 2025 prediction: rate"
            
            Return discussion after "####".
            """,
            agent=self.Regional_Pragmatists(),
            context=[
                self.regional_consolidated_analysis(),
                self.academic_consolidated_analysis(),
                self.central_consolidated_analysis(),
            ],
            expected_output="Concise, draft-style response from Regional Pragmatists to other members' analyses.",
        )

    @task
    def academic_discussion(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Respond to analyses with minimal steps, 30 words max per step.
            
            As Academic Balancers:
            1. Address key points from others
            2. Defend/clarify your position
            3. Note any mind changing
            4. Highlight theoretical considerations
            
            Format as:
            "Member point: agreement/disagreement; reason"
            "Position clarification: point; rationale"
            "Academic factors: concept; implication"
            "Updated leaning: solution; reason"
            "Updated 2025 prediction: rate"
            
            Return discussion after "####".
            """,
            agent=self.Academic_Balancers(),
            context=[
                self.regional_consolidated_analysis(),
                self.academic_consolidated_analysis(),
                self.central_consolidated_analysis(),
            ],
            expected_output="Concise, draft-style response from Academic Balancers to other members' analyses.",
        )

    @task
    def central_discussion(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Respond to analyses with minimal steps, 30 words max per step.
            
            As Central Policymakers:
            1. Address key points from others
            2. Defend/clarify your position
            3. Note any mind changing
            4. Highlight policy considerations
            
            Format as:
            "Member point: agreement/disagreement; reason"
            "Position clarification: point; rationale"
            "Policy factors: principle; implication"
            "Updated leaning: solution; reason"
            "Updated 2025 prediction: rate"
            
            Return discussion after "####".
            """,
            agent=self.Central_Policymakers(),
            context=[
                self.regional_consolidated_analysis(),
                self.academic_consolidated_analysis(),
                self.central_consolidated_analysis(),
            ],
            expected_output="Concise, draft-style response from Central Policymakers to other members' analyses.",
        )

    @task
    def regional_vote(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Cast final vote with minimal steps, 30 words max per step.
            
            As Regional Pragmatists, vote on:
            1. Preferred policy option
            2. Interest rate adjustment
            3. Historical comparisons (years)
            4. Specific metrics justification
            5. 2025 rate prediction (exact number)
            
            Format exactly as:
            Regional Pragmatist:
            POLICY VOTE: [Policy Option #]
            INTEREST RATE VOTE: [Rate adjustment]
            SPECIFIC HISTORICAL COMPARISONS: [years]
            EXPLANATION: [Metrics-based justification]
            PREDICTION FOR 2025: [Exact rate]
            
            Return vote after "####".
            """,
            agent=self.Regional_Pragmatists(),
            context=[
                self.regional_discussion(),
                self.academic_discussion(),
                self.central_discussion(),
            ],
            expected_output="Formatted vote from Regional Pragmatists following exact template format.",
        )

    @task
    def academic_vote(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Cast final vote with minimal steps, 30 words max per step.
            
            As Academic Balancers, vote on:
            1. Preferred policy option
            2. Interest rate adjustment
            3. Historical comparisons (years)
            4. Specific metrics justification
            5. 2025 rate prediction (exact number)
            
            Format exactly as:
            Academic Balancer:
            POLICY VOTE: [Policy Option #]
            INTEREST RATE VOTE: [Rate adjustment]
            SPECIFIC HISTORICAL COMPARISONS: [years]
            EXPLANATION: [Metrics-based justification]
            PREDICTION FOR 2025: [Exact rate]
            
            Return vote after "####".
            """,
            agent=self.Academic_Balancers(),
            context=[
                self.regional_discussion(),
                self.academic_discussion(),
                self.central_discussion(),
            ],
            expected_output="Formatted vote from Academic Balancers following exact template format.",
        )

    @task
    def central_vote(self) -> Task:
        return Task(
            description="""
            Use Chain of Draft: Cast final vote with minimal steps, 30 words max per step.
            
            As Central Policymakers, vote on:
            1. Preferred policy option
            2. Interest rate adjustment
            3. Historical comparisons (years)
            4. Specific metrics justification
            5. 2025 rate prediction (exact number)
            
            Format exactly as:
            Central Policymaker:
            POLICY VOTE: [Policy Option #]
            INTEREST RATE VOTE: [Rate adjustment]
            SPECIFIC HISTORICAL COMPARISONS: [years]
            EXPLANATION: [Metrics-based justification]
            PREDICTION FOR 2025: [Exact rate]
            
            Return vote after "####".
            """,
            agent=self.Central_Policymakers(),
            context=[
                self.regional_discussion(),
                self.academic_discussion(),
                self.central_discussion(),
            ],
            expected_output="Formatted vote from Central Policymakers following exact template format.",
        )

    @task
    def other_summary(self) -> Task:
        return Task(
            description="""
           Use Chain of Draft to extract information:
           
           1. Extract all historical years/dates
           2. Extract all metrics mentioned
           3. Format as JSON
           
           Steps:
           "Dates found: [list]"
           "Metrics found: [list]"
           "JSON: structure as required"
           
           Format exactly as:
           {{
               "exact_historical_dates_referenced": ["year1-year2", "year3-year4", ..., "year-year"],
               "exact_metrics_mentioned": ["Metric 1", "Metric 2", ..., "Metric n"]
           }}
           
           No text or explanations around JSON.
           Return JSON after "####".
           """,
            agent=self.analyst(),
            context=[
                self.regional_vote(),
                self.academic_vote(),
                self.central_vote(),
            ],
            expected_output="Clean JSON object with historical dates and metrics mentioned.",
        )

    @task
    def vote_summary(self) -> Task:
        return Task(
            description="""
           Use Chain of Draft to extract votes:
           
           1. Extract interest rate votes
           2. Format member votes as JSON
           
           Steps:
           "Regional vote: [extract]"
           "Academic vote: [extract]"
           "Central vote: [extract]"
           "JSON: structure as required"
           
           Format exactly as:
           {{
               "rate_votes": [
                   {{"member": "Regional Pragmatist", "vote": "#.##%"}},
                   {{"member": "Academic Balancer", "vote": "#.##%"}},
                   {{"member": "Central Policymaker", "vote": "#.##%"}}
               ]
           }}
           
           No text or explanations around JSON.
           Return JSON after "####".
           """,
            agent=self.analyst(),
            context=[
                self.regional_vote(),
                self.academic_vote(),
                self.central_vote(),
            ],
            expected_output="Clean JSON object with member votes.",
        )

    @task
    def prediction_summary(self) -> Task:
        return Task(
            description="""
           Use Chain of Draft to extract predictions:
           
           1. Extract 2025 rate predictions
           2. Format member predictions as JSON
           
           Steps:
           "Regional prediction: [extract]"
           "Academic prediction: [extract]"
           "Central prediction: [extract]"
           "JSON: structure as required"
           
           Format exactly as:
           {{
               "rate_predictions": [
                   {{"member": "Regional Pragmatist", "prediction": "#.##%"}},
                   {{"member": "Academic Balancer", "prediction": "#.##%"}},
                   {{"member": "Central Policymaker", "prediction": "#.##%"}}
               ]
           }}
           
           No text or explanations around JSON.
           Return JSON after "####".
           """,
            agent=self.analyst(),
            context=[
                self.regional_vote(),
                self.academic_vote(),
                self.central_vote(),
            ],
            expected_output="Clean JSON object with member predictions.",
        )

    @task
    def summary_final(self) -> Task:
        return Task(
            description="""
           Use Chain of Draft to combine summaries:
           
           1. Extract data from prior summaries
           2. Combine into single JSON object
           
           Steps:
           "Historical data: [extract]"
           "Metrics data: [extract]"
           "Votes data: [extract]"
           "Predictions data: [extract]"
           "Combined JSON: structure all together"
           
           Format exactly as:
           {{
               "exact_historical_dates_referenced": ["year1-year2", "year3-year4", ..., "year-year"],
               "exact_metrics_mentioned": ["Metric 1", "Metric 2", ..., "Metric n"],
               "rate_votes": [
                   {{"member": "Regional Pragmatist", "vote": "#.##%"}},
                   {{"member": "Academic Balancer", "vote": "#.##%"}}, 
                   {{"member": "Central Policymaker", "vote": "#.##%"}} 
               ],
               "rate_predictions": [
                   {{"member": "Regional Pragmatist", "prediction": "#.##%"}},
                   {{"member": "Academic Balancer", "prediction": "#.##%"}}, 
                   {{"member": "Central Policymaker", "prediction": "#.##%"}}
               ]
           }}
           
           No text or explanations around JSON.
           """,
            agent=self.analyst(),
            context=[
                self.other_summary(),
                self.vote_summary(),
                self.prediction_summary(),
            ],
            expected_output="Clean combined JSON object with all summary data.",
            output_file="rate_summary.json",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FOMC simulation crew with Chain of Draft"""
        return Crew(
            agents=[
                self.economist(),
                self.Regional_Pragmatists(),
                self.Academic_Balancers(),
                self.Central_Policymakers(),
                self.analyst(),
            ],
            tasks=[
                # Individual knowledge source analysis tasks
                self.analyze_current_macro(),
                self.analyze_historical_macro(),
                self.probabilities_comment(),
                
                # Regional Pragmatists individual knowledge analysis
                self.regional_beige_book_analysis(),
                self.regional_current_macro_analysis(),
                self.regional_historical_analysis(),
                
                # Academic Balancers individual knowledge analysis
                self.academic_dot_plot_analysis(),
                self.academic_current_macro_analysis(),
                self.academic_historical_analysis(),
                
                # Central Policymakers individual knowledge analysis
                self.central_fed_explanation_analysis(),
                self.central_current_macro_analysis(),
                self.central_historical_analysis(),
                
                # Economist proposals based on individual analyses
                self.get_economic_suggestions(),
                
                # Consolidated analyses from each group
                self.regional_consolidated_analysis(),
                self.academic_consolidated_analysis(),
                self.central_consolidated_analysis(),
                
                # Discussion phase
                self.regional_discussion(),
                self.academic_discussion(),
                self.central_discussion(),
                
                # Voting phase
                self.regional_vote(),
                self.academic_vote(),
                self.central_vote(),
                
                # Summary phase
                self.other_summary(),
                self.vote_summary(),
                self.prediction_summary(),
                self.summary_final(),
            ],
            process=Process.sequential,  
            verbose=True,
            memory=True,
            output_log_file="fomc_simulation.md",
        )