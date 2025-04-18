import cv2
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_frame_by_time(timestamp: float) -> dict:
    """Extracts a frame from the video file at the specified timestamp.

    Args:
        timestamp (float): Timestamp in seconds to extract the frame from

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
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        if timestamp < 0 or timestamp > duration:
            return {
                "status": "error",
                "error_message": f"Timestamp {timestamp}s is outside video duration of {duration:.2f}s"
            }
            
        # Convert timestamp to frame number
        frame_number = int(timestamp * fps)
        
        # Set frame position and read the frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return {
                "status": "error",
                "error_message": f"Failed to extract frame at timestamp {timestamp}s"
            }
        
        # Create a temporary file with .png extension
        temp_dir = tempfile.gettempdir()
        temp_image_path = os.path.join(temp_dir, f"frame_{timestamp}s.png")
        
        # Save the frame as PNG
        cv2.imwrite(temp_image_path, frame)
        
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        return {
            "status": "success",
            "report": f"Frame at {timestamp}s (frame #{frame_number}) extracted successfully from {video_path}. Dimensions: {width}x{height}. Saved to: {temp_image_path}",
            "image_path": temp_image_path
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error extracting frame: {str(e)}"
        }