# Webcam Hand Gesture Drawing and AI Interaction

This project uses OpenCV, Google Generative AI, and HandTracking to create a gesture-based drawing application with AI integration. The program detects hand gestures to perform actions like drawing, erasing, and solving math problems using the webcam feed. It processes the gestures using a hand tracking module and sends the drawing to a generative AI model for further interaction.

## Requirements

### Python Libraries:
- `cvzone`: For hand tracking.
- `cv2`: For capturing webcam feed and processing images.
- `numpy`: For image processing.
- `google.generativeai`: For integrating with Google Generative AI model.
- `PIL` (Python Imaging Library): For converting numpy arrays to image format.

Install the required libraries using pip:

```bash
pip install opencv-python cvzone google-generativeai numpy pillow
```
# Setup
Install Python and Dependencies
Ensure you have Python 3.x installed on your machine. Use the following command to install necessary libraries:

```
pip install opencv-python cvzone google-generativeai numpy pillow
```

Google API Key
You'll need a valid Google API key for accessing the Generative AI model. Replace the API key in the code with your own API key.

`genai.configure(api_key="YOUR_API_KEY")`
Webcam Setup
The program uses your webcam to detect hand gestures. Ensure your webcam is connected and working.

How It Works
1. Hand Gesture Detection
The program uses the HandDetector from the cvzone library to detect hand gestures. Based on the gestures, different actions are triggered:

Drawing: When the thumb and index finger are raised ([0, 1, 0, 0, 0]), the program draws on the screen where the tip of the index finger is located.

Erasing: When only the thumb is raised ([1, 0, 0, 0, 0]), the screen is cleared.

Math Problem Solving: When the middle, ring, and pinky fingers are raised ([0, 0, 1, 1, 1]), the current drawing is sent to Google Generative AI for solving a math problem.

2. Drawing on Canvas
When the user makes the drawing gesture, the program draws on a transparent canvas. The canvas is then combined with the live webcam feed to display the drawing.

3. Interaction with Google Generative AI
When the user triggers the math-solving gesture, the drawing on the canvas is sent to the Google Generative AI model. The AI then responds with the result, which is printed in the console.

4. Exit Button
A "THOAT" button is displayed on the screen. If clicked, the program exits.

5. Exit Key
Press the "q" key to exit the application.

Code Overview
getHandInfo(img):
Detects hand gestures and returns the position of the fingers and landmarks of the hand.

draw(info, prev_pos, canvas):
Draws on the canvas based on hand gestures. It also handles the erasing functionality.

sendToAI(model, canvas, fingers):
Sends the current canvas image to the AI model if the math-solving gesture is detected.

Main Loop:
Captures the webcam feed, detects hand gestures, and performs actions like drawing and interacting with the AI.

Running the Program
Run the script:

```
python hand_gesture_ai.py
```
Webcam Feed will open. You can:

Draw: Raise your thumb and index finger.

Erase: Raise only your thumb.

Solve Math Problem: Raise the middle, ring, and pinky fingers.

Exit the Application by pressing the "q" key or clicking the "THOAT" button.

Troubleshooting
API Key Error:
Ensure that your Google API key is valid. Replace the default API key with your own in the code.

Webcam Not Detected:
Check if your webcam is properly connected and accessible.

Module Not Found Error:
If you get a ModuleNotFoundError, ensure that all required libraries are installed using the pip command.
