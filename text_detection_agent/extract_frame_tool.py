import cv2
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_frame_tool(frame_number: int) -> dict:
    """Extracts a specific frame from the video file specified in .env and saves it as an image.

    Args:
        frame_number (int): Frame number to extract (0-based index)

    Returns:
        dict: status and result or error msg with saved image path
    """
    try:
        # Get video file name from environment variables
        video_file_name = os.getenv('VIDEO_FILE_NAME')
        if not video_file_name:
            return {
                "status": "error",
                "error_message": "VIDEO_FILE_NAME not found in environment variables"
            }
            
        # Use the video file from the current directory
        video_path = os.path.join(os.path.dirname(__file__), video_file_name)
        
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "error_message": f"Video file not found at: {video_path}"
            }

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        
        # Get total number of frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if frame_number >= total_frames:
            return {
                "status": "error",
                "error_message": f"Frame number {frame_number} exceeds total frames {total_frames}"
            }
        
        # Set frame position and read the frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return {
                "status": "error",
                "error_message": f"Failed to extract frame {frame_number}"
            }
        
        # Create a temporary file with .png extension
        temp_dir = tempfile.gettempdir()
        temp_image_path = os.path.join(temp_dir, f"frame_{frame_number}.png")
        
        # Save the frame as PNG
        cv2.imwrite(temp_image_path, frame)
        
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        return {
            "status": "success",
            "report": f"Frame {frame_number} extracted successfully from {video_path}. Dimensions: {width}x{height}. Saved to: {temp_image_path}",
            "image_path": temp_image_path
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error extracting frame: {str(e)}"
        }