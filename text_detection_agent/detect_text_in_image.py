import cv2
import easyocr
import os

# Initialize the OCR reader globally
reader = easyocr.Reader(['en', 'ro'])

def detect_text_in_image(image_path: str) -> dict:
    """Detects and recognizes text in an image.

    Args:
        image_path (str): Path to the image file to analyze

    Returns:
        dict: status and result or error msg.
    """
    try:
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "error_message": f"Image file not found at: {image_path}"
            }

        # Read the image
        frame = cv2.imread(image_path)
        if frame is None:
            return {
                "status": "error",
                "error_message": f"Failed to read image: {image_path}"
            }
        
        # Convert BGR to RGB for easyocr
        # easyocr expects images in RGB format, while OpenCV reads them in BGR format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect text
        results = reader.readtext(frame_rgb)
        
        # Process all results regardless of confidence
        text_results = []
        for bbox, text, confidence in results:
            text_results.append({
                "text": text,
                "confidence": f"{confidence * 100:.2f}%",
                "location": f"({int(bbox[0][0])}, {int(bbox[0][1])}) to ({int(bbox[2][0])}, {int(bbox[2][1])})"
            })
        
        if not text_results:
            return {
                "status": "success",
                "report": "No text detected in the image."
            }
        
        report = "Detected text:\n" + "\n".join(
            f"'{result['text']}' (Confidence: {result['confidence']}, Location: {result['location']})"
            for result in text_results
        )
        
        return {
            "status": "success",
            "report": report
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error detecting text: {str(e)}"
        }