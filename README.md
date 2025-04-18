# Text Detection Agent

A Python-based agent that provides tools for extracting frames from videos and performing text detection on them. This project combines OpenCV for frame extraction and EasyOCR for text detection.

## Features

- Extract specific frames from video files using frame index or timestamp
- Detect and recognize text in images with confidence scores
- Environment-based configuration for easy setup
- Built-in support for both English and Romanian text detection
- Integration with Google's Gemini models (additional models available through VertexAI)

## Model Support

Currently, this implementation supports Google's Gemini models by default, using 'gemini-2.0-flash'. To use other AI models, you'll need to:
1. Set up Google Cloud VertexAI
2. Set `GOOGLE_GENAI_USE_VERTEXAI=TRUE` in your environment
3. Configure appropriate VertexAI credentials

## Requirements

- Python 3.x
- OpenCV (cv2)
- EasyOCR
- python-dotenv
- Google ADK

## Installation

1. Clone the repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and configure your environment:
   ```bash
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY='your-api-key'
   VIDEO_FILE_NAME='your-video-file-name'
   MODEL_NAME='gemini-2.0-flash'  # Optional, this is the default
   ```

## Usage

The agent provides three main tools:

### Frame Extraction Tools

```python

# Extract frame by index (0-based)
result = extract_frame_by_index(1250)
if result["status"] == "success":
    print(result["report"])
    frame_path = result["image_path"]

# Extract frame at specific timestamp (in seconds)
result = extract_frame_by_time(42)
if result["status"] == "success":
    print(result["report"])
    frame_path = result["image_path"]
```

### Text Detection Tool

```python
from text_detection_agent.detect_text_in_image import detect_text_in_image

# Detect text in an image
result = detect_text_in_image("path/to/image.png")
if result["status"] == "success":
    print(result["report"])
```

## Tool Response Format

All tools return a dictionary with the following structure:

```python
{
    "status": "success" | "error",
    "report": str,  # Success message or detailed results
    "error_message": str,  # Only present if status is "error"
    "image_path": str,  # Only present in frame extraction tool success responses
}
```

## Example Workflow

Extract a frame and perform text detection:
```python
frame_result = extract_frame_by_index(1250)  # or extract_frame_by_time(42)
if frame_result["status"] == "success":
    # Use the extracted frame for text detection
    text_result = detect_text_in_image(frame_result["image_path"])
    if text_result["status"] == "success":
        print(text_result["report"])
```

## Configuration

The project uses environment variables for configuration:

- `VIDEO_FILE_NAME`: Name of the video file to process (must be in the project directory)
- `MODEL_NAME`: The AI model to use for the agent (defaults to 'gemini-2.0-flash')
- `GOOGLE_API_KEY`: Your Google API key for authentication
- `GOOGLE_GENAI_USE_VERTEXAI`: Flag to determine whether to use VertexAI

## Error Handling

All tools include comprehensive error handling for common scenarios:
- File not found errors
- Invalid frame numbers or timestamps
- Image reading failures
- Text detection errors
- Environment configuration issues

## Dependencies

- OpenCV: Video and image processing
- EasyOCR: Text detection and recognition (pre-configured for English and Romanian)
- python-dotenv: Environment configuration
- Google ADK: Agent Development Kit for the AI interface

## Running the Agent

There are multiple ways to interact with the agent using ADK:

### 1. Using the Dev UI (Recommended for Development)

1. Navigate to the parent directory of the agent project:
   ```bash
   cd ..
   ```

2. Run the following command to launch the dev UI:
   ```bash
   adk web
   ```

3. Open the URL provided (usually http://localhost:8000 or http://127.0.0.1:8000) in your browser.

4. In the top-left corner of the UI, select "video_frame_analyzer" from the dropdown menu.

5. You can now interact with your agent through:
   - Text chat in the input box
   - Inspecting individual function calls and responses
   - Using voice interaction (requires Gemini models that support Live API)
Note: For voice/video streaming features in the Dev UI, you'll need to use Gemini models that support the Live API.

### 2. Using the Terminal

You can run the agent directly in the terminal:
```bash
adk run
```

### 3. Running as an API Server

For integration with other applications, you can run the agent as an API server:
```bash
adk api_server
```

### Example Prompts

Examples of prompts to query the agent:
- "Show me capabilities and limitations of the agent"
- "Extract frame 1250 from the video"
- "Get the frame at 42 seconds into the video"
- "Detect text in the extracted frame"
- "Extract frame 11350 and analyze it for text"
- "Extract and compare the text results for frame 1230 and 1250"