# BnyCapstoneCrew Crew

Welcome to the BnyCapstoneCrew Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/bny_capstone_crew/config/agents.yaml` to define your agents
- Modify `src/bny_capstone_crew/config/tasks.yaml` to define your tasks
- Modify `src/bny_capstone_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/bny_capstone_crew/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the bny_capstone_crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The bny_capstone_crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the BnyCapstoneCrew Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.


### Here are three consolidated FOMC voting members that encapsulate the personalities and decision-making patterns of the original 12 members:

### 1. Chair Jerome Powell (Consensus Leader)
Role: Chair of the Federal Open Market Committee
Goal: Ensure monetary policy aligns with long-term economic stability, balancing inflation control and labor market resilience.
Backstory: Powell has led the Fed through economic crises, including COVID-19 and the Great Inflation Reversal. He balances aggressive inflation control (Volcker-style) with employment protection (Bernanke-style).
Decision Factors: Beige Book insights, inflation risks, labor market trends.
Likely Vote: Leans toward consensus but prefers stability; cautious on rate cuts unless inflation is clearly under control.

### 2. Vice Chair John Williams (Data-Driven Economist)
Role: Vice Chair of the Federal Reserve
Goal: Use quantitative models and historical Fed policy cycles to guide interest rate decisions.
Backstory: Williams emphasizes empirical data, referencing global central banks and past rate cycles. He values inflation persistence metrics and soft-landing strategies (1990s).
Decision Factors: CPI/PCE inflation data, global monetary trends, employment softness.
Likely Vote: Supports cuts if inflation data trends downward and unemployment worsens.

### 3. Regional & Regulatory Representative (Economic Field Perspective)
Role: Represents regional economies, financial stability, and banking system health.
Goal: Balance the needs of labor markets, small businesses, and financial institutions.
Backstory: Inspired by Bostic, Barkin, Barr, and Kugler, this representative monitors the banking sector (post-2008 reforms), regional labor markets (job trends), and global competitiveness (capital flows).
Decision Factors: Unemployment spikes, credit liquidity concerns, global rate adjustments.
Likely Vote: Pushes for cuts if regional economic strain or banking liquidity risks emerge.

### How These Three Capture the Original 12:
Powell represents the stabilizers (himself, Bowman, Daly, Waller).
Williams represents the data-driven economists (Cook, Jefferson, Kugler).
The third agent integrates regional perspectives, financial stability concerns, and global trends (Bostic, Barkin, Barr, and others).
This setup ensures the voting dynamics still reflect the broader FOMC’s policy inclinations.