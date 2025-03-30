# Below setup ensures an automated pipeline for researching and writing about "Medical Industry using Generative AI". 🚀

# Environment Setup & Imports
# CrewAI Modules:
# 1. Agent → Represents AI agents with distinct roles
# 2. Crew → Manages multiple agents and their tasks
# 3. LLM → Defines the language model used by agents
# 4. Task → Defines specific actions agents will perform

from crewai import Agent, Crew, LLM, Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Loads API keys from a .env file
load_dotenv()

# topic definition
topic = "Medical industry using Generative AI"


# LLM - Specifies GPT-4 as the language model for both agents
llm = LLM(model="gpt-4")

# Tools - SerperDevTool → Enables live web searches for research
# n=1 → The tool will return 1 search result per query
search_tool = SerperDevTool(n=1)



## Define AI Agents and its parameters:
# role             - Defines the agent’s role (e.g., Research Analyst, Content Writer)
# goal             - Specifies the main objective of the agent
# backstory        - Provides context for the agent’s skills, expertise, and behavior
# allow_delegation - If True, the agent can delegate tasks to others. If False, it must complete tasks itself
# tools	           - List of tools the agent can use (e.g., web search tools)
# llm              - Defines the language model (e.g., GPT-4) used by the agent
# verbose          - If True, it enables detailed logging for debugging

# Agent 1
senior_research_analyst = Agent(
    role="Senior Research Analyst",
    goal=f"Research, analyze and synthesize comprehensive information on {topic} from reliable web sources",
    backstory=  "You are an expert research analyst with advanced web research skills. You excel at finding "
                "analyzing and synthesizing information from across the internet using search tools. You are "
                "skilled at distinguishing reliable sources from unreliable ones, fact-checking, " 
                "cross-referencing information and identifying key patterns and insights. You provide "
                "well-oranized research briefs with proper citations and source verification. Your analysis "
                "includes both raw data and interpreted insights, making complex information accessible and "
                "actionable",
    allow_delegation = False, # The agent cannot pass tasks to others
    tools=[search_tool], # Uses the SerperDevTool for live web search
    ll=llm, # Uses GPT-4 for processing
    verbose=True  # Enable logging for debugging
)


# Agent 2
content_writer = Agent(
    role="Content Writer",
    goal="Transform research findings into engaging blog posts while maintaining accuracy",
    backstory=  "You are a skilled content writer specialised in creating engaging accessible content from "
                "technical research. You work closely with the Senior Research Analyst and excel at maintaining "
                "the perfect balance between informative and entertaining writing while ensuring all facts and "
                "citations from the research are properly incorporated. You have a talent for making complex "
                "topics approachable without oversimplifying them",
    allow_delegation = False, # cannot pass tasks to others.
    llm=llm, # Uses GPT-4 for content generation
    verbose=True  # Enable logging for debugging
)


## Define AI tasks and its parameters:
# description     -	Details what the task should accomplish
# expected_output -	Defines what the task output should look like
# agent	          - Assigns the task to a specific agent

# Task 1 - Research Task
research_tasks = Task(
    description=(""""
        1. Conduct comprehensive research on {topic} including:
        - Recent developments and news
        - Key industry Trends and innovations
        - Expert opinions and analysis
        - Statistical data and market insights
        2. Evaluate source credibility and fact-check all information 
        3. Organised findings into a structured research brief
        4. Include all relevant citations and sources
        """),
    expected_output = """A detailed Research report containing:
            - Executive summary of key findings 
            - Comprehensive analysis of current trends and developments 
            - List of verified facts and Statistics
            - All citations and links to original sources 
            - Clear categorisation of main themes and patterns
            Please format with clear sections and Bullet points for easy references.""",
    agent = senior_research_analyst
)

# Task 2 - Content Writing
writing_tasks = Task(
    description=(""""
                Using the research brief provided create an engaging block post that:
                1. Transforms technical information into accessible content 
                2. Maintains all factual accuracy and citizens from the research 
                3. Includes:
                    - Attention-grabbing introduction
                    - Well structured-body sections with clear headings
                    - Compelling conclusion 
                4. Preserves all sources citations in [Source: URL] format 
                5. Includes a References section at the end
    """),
    expected_output = """A polished blog post in markdown format that:
                - Engages readers while maintain accuracy 
                - Contains properly structured sections 
                - Includes inline citations hyperlinked to the original source URL 
                - Presents information in an accessible yet informative way 
                - Follows proper markdown formatting, use H1 for the title and H3 for the sub-sections""",
    agent = content_writer
)


# Creates a Crew with:
# 1. The Senior Research Analyst (research task)
# 2. The Content Writer (writing task)
crew = Crew(
    agents = [senior_research_analyst, content_writer],
    tasks = [research_tasks, writing_tasks],
    verbose = True
)


result = crew.kickoff(inputs={"topic": topic})

print(result)