from crewai import Agent, Crew, LLM, Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

topic = "Medical industry using Generative AI"


# LLM
llm = LLM(model="gpt-4")

# Tools
search_tool = SerperDevTool(n=1)


# Agent 1
senior_research_analyst = Agent(
    role="Senior Research Analyst",
    goal=f"Research, analyze and synthesize comprehensive information on {topic} from reliable web sources",
    backstory=  "You are an expert research analyst with advanced web research skills. You excel at finding "
                "analyzing and synthesizing information from across the internet using search tools. You are "
                "skilled at distinguishing reliable sources from unreliable ones, fact-checking, " 
                "cross-referencing information and indentifying key patterns and insights. You provide "
                "well-oranized research briefs with proper citations and source verification. Your analysis "
                "includes both raw data and interpreted insights, making complex information accessible and "
                "actionable",
    allow_delegation = False,
    tools=[search_tool],
    ll=llm,
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
    allow_delegation = False,
    llm=llm,
    verbose=True  # Enable logging for debugging
)




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



crew = Crew(
    agents = [senior_research_analyst, content_writer],
    tasks = [research_tasks, writing_tasks],
    verbose = True
)


result = crew.kickoff(inputs={"topic": topic})

print(result)