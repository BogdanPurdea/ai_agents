from google.adk.agents import Agent
from .extract_frame_by_index import extract_frame_by_index
from .extract_frame_by_time import extract_frame_by_time
from .detect_text_in_image import detect_text_in_image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

root_agent = Agent(
    name="video_frame_analyzer",
    model=os.getenv('MODEL_NAME', 'gemini-2.0-flash'),  # Default fallback if not set in .env
    description=(
        "Agent to extract frames from video and analyze them for text content."
    ),
    instruction=(
        "You are a helpful agent who can extract frames from video files "
        "using either frame numbers or timestamps, and analyze them for text "
        "content with high confidence score(>85%)."
    ),
    tools=[extract_frame_by_index, extract_frame_by_time, detect_text_in_image],
)