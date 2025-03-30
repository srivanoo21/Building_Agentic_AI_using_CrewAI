# Importing Dependencies
from crewai import Agent, Crew, LLM, Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


## Setting Up Streamlit UI

# Streamlit page config
st.set_page_config(page_title="Content Researcher & Writer", page_icon="🍎", layout="wide")
# Title and description
st.title("🍏 Content Researcher & Writer, powered by CrewAI")
st.markdown("Generate blog posts about any topic using AI agents.")


# Sidebar
with st.sidebar:
    st.header("Content Settings")

    # Make the text input take up more space
    topic = st.text_area(
        "Enter your topic",
        height = 100,
        placeholder = "Enter the topic"
    )

    # Add more sidebar controls if needed
    st.markdown("### LLM Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

    # Add some spacing
    st.markdown("---")

    # Make the generate button more prominent in the sidebar
    generate_button = st.button("Generate Content", type="primary", use_container_width=True)

    # Add some helpful information
    with st.expander("How to use"):
        st.markdown("""
                    1. Enter your desired content topic
                    2. Play with the temperature
                    3. Click "Generate Content" to start
                    4. Wait for the AI to generate your article
                    5. Download the result as a markdown file
                    """)

# Generating Content with CrewAI
def generate_content(topic):
    """
    Generates AI-powered content based on the given topic.

    This function initializes the LLM model, sets up AI agents for research and content writing, 
    assigns them specific tasks, and executes them using CrewAI.

    Parameters:
    topic (str): The subject for which the content should be generated.

    Returns:
    str: The generated blog post in markdown format.
    """
    
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


    return crew.kickoff(inputs={"topic": topic})


# Main content area
# This section handles the main content generation process. When the "Generate Content" button is clicked, it #triggers the generate_content function, displays a loading spinner, and presents the generated text with a download option while handling potential errors.
if generate_button:
    with st.spinner("Generating content... This may take a moment."):
        try:
            result = generate_content(topic)
            st.markdown("### Generated content")
            st.markdown(result)

            # Add download button
            st.download_button(
                label="Download Content",
                data=result.raw,
                file_name = f"{topic.lower().replace(' ', '_')}_article.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with CrewAI, Streamlit and ChatGPT")