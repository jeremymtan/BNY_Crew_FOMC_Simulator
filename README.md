# Multi-Agent Framework for FOMC Simulation

Welcome to the BnyCapstoneCrew Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

# Table of Contents

- [Multi-Agent Framework for FOMC Simulation](#multi-agent-framework-for-fomc-simulation)
- [Summary](#summary)
- [Motivation & Goals](#motivation--goals)
- [High-Level Overview](#high-level-overview)
- [Installation and Setup](#installation-and-setup)
  - [Running the Project](#running-the-project)
  - [Backtesting a meeting](#backtesting-a-meeting)
- [Methodology](#methodology)
  - [1. Quantitative Modeling](#1-quantitative-modeling)
  - [2. LLM-Based Multi-Agent Simulation](#2-llm-based-multi-agent-simulation)
  - [3. Clustering](#3-clustering)
    - [FOMC Voting Members](#here-are-three-consolidated-fomc-voting-members-that-encapsulate-the-personalities-and-decision-making-patterns-of-the-original-12-members)
  - [4. Chain of Draft Simulation](#4-chain-of-draft-simulation)
- [Investigations & Results](#investigations--results)
  - [Evaluation Metrics](#1-average-rate-change-accuracy)
  - [Key Results + Interpretation](#key-results--interpretation)
- [Connecting Back to Goals](#connecting-back-to-goals)
- [References](#references)

## Summary

This project aims to simulate the Federal Open Market Committee’s (FOMC) decision-making process using **large language models (LLMs)** embedded within a **multi-agent architecture**. We seek to improve **federal funds rate prediction accuracy** and interpretability—key for risk management at BNY. Traditional models fail to capture the deliberative and human-like reasoning embedded in FOMC decisions. Our framework leverages economic data, unstructured inputs (e.g., Beige Book, dot plots), and agent discussions to emulate realistic monetary policy decisions.

## Motivation & Goals

**Why does this matter?**  
BNY’s financial health is directly influenced by Federal Funds Rate decisions. Traditional predictive models lack transparency and adaptability. Our goal is to:

- Predict the **FOMC’s interest rate decisions**
- **Understand** the reasoning behind decisions using a transparent multi-agent simulation
- Offer a **framework that can be integrated** into BNY’s internal models (e.g., Eliza)


## High-Level Overview

The project evolved across three modeling stages:

1. **Linear Regression Baseline** using macroeconomic data  
2. **Multi-Agent Simulation** modeling FOMC participants via LLMs  
3. **Chain of Draft Prompting (CoD)** to reduce token cost and improve deliberation quality  

Each agent receives data, discusses implications, and votes, mimicking the FOMC decision process. We use clustering to reduce agent complexity while retaining realism.

## Installation and Setup 

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, in the any of the directories run 
```bash
pip install -r requirements.txt
```
**DO NOT CREATE YOUR OWN VIRTUAL ENVIRONMENT**

Enter any of the directories and lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

**Add your `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, etc into the `.env` file**


### Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the bny_capstone_crew directory:

```bash
$ crewai run
```

This command initializes the bny_capstone_crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

### Backtesting a meeting
Once you have successfully completed a single run, you may automate 5 runs of a given meeting. **Ensure that you update crew.py and Automated_metrics.py to have the correct meeting date and correct_vote variable.**

run this from the bny_capstone_crew directory:
```bash
$ chmod +x run_crew.sh
```
and any time you change any scripts, rerun the above CLI before running:

```bash
$ ./run_crew.sh
```

**The output will be in results.txt, but check all 5 summary json files to ensure formatting**

##  Methodology

### 1. Quantitative Modeling

- **Inputs:** CPI, PCE, VIX, Treasury Bill yields, unemployment, party control, etc.
- **Output:** Interest rate change (e.g., +0.25%)
- **Model:** Linear Regression  
  - Accuracy: **57.14%**
  - Balanced Test Set: **33.3%**

### 2. LLM-Based Multi-Agent Simulation

- Agents emulate FOMC personas (e.g., Regional Pragmatist, Central Policymaker)
- Input includes **structured** and **unstructured** data:
  - Beige Book
  - Dot Plots
  - Fed Funds Futures Probabilities
- uses sequential prompting
- base model does not include long term simulation memory, but base + simulation does
- You can find it here: [base folder](./base/) and [simulation + base folder](./base_simulation/)
### 3. Clustering

- KNN-based grouping using:
  - Political affiliation
  - Gender
  - Tenure
- Reduces the agent count while preserving diversity of views


#### Here are three consolidated FOMC voting members that encapsulate the personalities and decision-making patterns of the original 12 members:

### 1. Chair Jerome Powell (Consensus Leader)
- **Role:** Chair of the Federal Open Market Committee
- **Goal:** Ensure monetary policy aligns with long-term economic stability, balancing inflation control and labor market resilience.
- **Backstory:** Powell has led the Fed through economic crises, including COVID-19 and the Great Inflation Reversal. He balances aggressive inflation control (Volcker-style) with employment protection (Bernanke-style).
- **Decision Factors:** Beige Book insights, inflation risks, labor market trends.
- **Likely Vote:** Leans toward consensus but prefers stability; cautious on rate cuts unless inflation is clearly under control.

### 2. Vice Chair John Williams (Data-Driven Economist)
- **Role:** Vice Chair of the Federal Reserve
- **Goal:** Use quantitative models and historical Fed policy cycles to guide interest rate decisions.
- **Backstory:** Williams emphasizes empirical data, referencing global central banks and past rate cycles. He values inflation persistence metrics and soft-landing strategies (1990s).
- **Decision Factors:** CPI/PCE inflation data, global monetary trends, employment softness.
- **Likely Vote:** Supports cuts if inflation data trends downward and unemployment worsens.

### 3. Regional & Regulatory Representative (Economic Field Perspective)
- **Role:** Represents regional economies, financial stability, and banking system health.
- **Goal:** Balance the needs of labor markets, small businesses, and financial institutions.
- **Backstory:** Inspired by Bostic, Barkin, Barr, and Kugler, this representative monitors the banking sector (post-2008 reforms), regional labor markets (job trends), and global competitiveness (capital flows).
- **Decision Factors:** Unemployment spikes, credit liquidity concerns, global rate adjustments.
- **Likely Vote:** Pushes for cuts if regional economic strain or banking liquidity risks emerge.

### How These Three Capture the Original 12:
- Powell represents the stabilizers (himself, Bowman, Daly, Waller).
- Williams represents the data-driven economists (Cook, Jefferson, Kugler).
- he third agent integrates regional perspectives, financial stability concerns, and global trends (Bostic, Barkin, Barr, and others).
*This setup ensures the voting dynamics still reflect the broader FOMC’s policy inclinations.*


### 4. Chain of Draft Simulation

- Adds memory, reflection, and iterative voting
- Uses sequential prompting 
- Inspired by *Xu et al. (2025)*
- You can find it here: [chain of draft folder](./chain_of_draft/) 

## Investigations & Results

- **Backtesting across 9 meetings (2023–2025)** with 5 runs per meeting
- **Metrics Evaluated:**
  - Overall rate prediction accuracy
  - Individual agent voting accuracy
  - Voting stability across runs

#### 1. Average Rate Change Accuracy
Whether the model correctly predicts the overall rate decision for each meeting.

$$
\text{Average Rate Change Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \mathbf{1}\left(\hat{\text{Vote}}_i = \text{Vote}^*_i\right)
$$

---

#### 2. Average Individual Voting Accuracy  
Whether each agent correctly predicts the true rate decision in each meeting.

$$
\text{Average Individual Voting Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \left( \frac{1}{K} \sum_{k=1}^{K} \mathbf{1}\left(\hat{\text{Vote}}_{i,k} = \text{Vote}^*_i\right) \right)
$$

---

#### 3. Average Voting Stability  
Evaluates the consistency of model predictions for individual agent votes across simulation runs for each meeting.

$$
\text{Average Voting Stability} = \frac{1}{NJK} \sum_{i=1}^{N} \sum_{j=1}^{J} \sum_{k=1}^{K} \mathbf{1} \left( \hat{V}_{i,j,k} = \text{mode}(\hat{V}_{i,\cdot,k}) \right)
$$

---

![Results](https://github.com/user-attachments/assets/e2616f4f-b1d9-4fcd-aff1-bc6c9a668de9)


###  Key Results + Interpretation 

- **Simulation improved predictive accuracy by 56% over the baseline model.**  
  The baseline linear regression achieved a 33% accuracy rate on a balanced test set, while the simulation-enhanced multi-agent model reached up to 89% accuracy. This suggests that agent-based reasoning paired with structured and unstructured inputs (e.g., Beige Book, dot plots) enables more accurate modeling of FOMC decision-making dynamics.

- **All multi-agent models exhibited 70–80% voting stability across repeated simulations.**  
  We evaluated voting stability by measuring how consistently agents voted across five runs per meeting. High stability indicates the model is not overly sensitive to prompt randomness or internal variation—critical for building stakeholder trust in model outputs.

- **Chain of Draft (CoD) architecture offered better interpretability and reduced token usage,**  
  particularly helpful for working with longer inputs like the Beige Book. The sequen



###  Connecting Back to Goals

Our primary objective was to create a framework that could not only **predict Federal Funds Rate decisions** but also **explain the reasoning** behind those predictions—something traditional models fail to deliver. The simulation-based multi-agent framework achieves this by modeling FOMC participants as LLM-powered agents who deliberate, reflect, and vote based on both structured and unstructured inputs.

By improving prediction accuracy by **56%** and demonstrating **high voting stability**, our models fulfill the dual goal of **reliability** and **interpretability**. The inclusion of memory-based reasoning and Chain of Draft prompting further aligns with our aim to make the decision process **transparent, modular, and extensible**.

This approach lays the foundation for BNY to:
- Validate and enhance their internal models (e.g., Eliza),
- Incorporate real-world economic nuance into forecasting pipelines,
- And support internal risk and rate strategy teams with **interpretable agent-driven simulations**.

In short, we’ve moved from static prediction to **dynamic simulation**, delivering a system that reflects the complex, human-like reasoning that defines real-world FOMC decision-making.



### References

1. Li, P., Castelo, N., Katona, Z., & Sarvary, M. (2024). *Frontiers: Determining the validity of large language models for automated perceptual analysis.* Marketing Science, 43(2), 254–266.

2. Xu, S., Xie, W., Zhao, L., & He, P. (2025). *Chain of Draft: Thinking Faster by Writing Less.* arXiv preprint. [arXiv:2502.18600](https://arxiv.org/abs/2502.18600)

3. Seok, S., Wen, S., Yang, Q., Feng, J., & Yang, W. (2024). *MiniFed: Integrating LLM-based Agentic-Workflow for Simulating FOMC Meeting.* arXiv preprint. [arXiv:2410.18012](https://arxiv.org/abs/2410.18012)

4. Park, J. S., O’Brien, J., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). *Generative agents: Interactive simulacra of human behavior.* In *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology* (pp. 1–22).

5. Federal Reserve. (n.d.). *FOMC meeting calendars, statements, and minutes.* Retrieved February 2, 2025, from [https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)

6. CME Group. (n.d.). *CME FedWatch Tool.* Retrieved February 15, 2025, from [https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html](https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html)

7. Tadle, R. C. (2022). *FOMC minutes sentiments and their impact on financial markets.* Journal of Economics and Business, 118, 106021. [https://doi.org/10.1016/j.jeconbus.2021.106021](https://doi.org/10.1016/j.jeconbus.2021.106021)

8. Ruman, A. M. (2023). *A comparative textual study of FOMC transcripts through inflation peaks.* Journal of International Financial Markets, Institutions and Money, 87, 101822. [https://doi.org/10.1016/j.intfin.2023.101822](https://doi.org/10.1016/j.intfin.2023.101822)






