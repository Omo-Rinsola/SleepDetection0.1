from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import cv2
import mediapipe as mp
import numpy as np
import base64
import json


# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Eye landmarks indices for EAR calculation
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]


def calculate_ear(eye_landmarks):
    """Calculate Eye Aspect Ratio (EAR) for drowsiness detection."""
    # Vertical distances
    v1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
    v2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])

    # Horizontal distance
    h = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])

    # EAR formula
    ear = (v1 + v2) / (2.0 * h)
    return ear


def detect_sleep_status(frame):
    """Process frame and detect sleep status using MediaPipe."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if not results.multi_face_landmarks:
        return "no-face-detected"

    face_landmarks = results.multi_face_landmarks[0]
    h, w, _ = frame.shape

    # Extract eye landmarks
    left_eye_points = np.array([(face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h) for i in LEFT_EYE])
    right_eye_points = np.array([(face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h) for i in RIGHT_EYE])

    # Calculate EAR for both eyes
    left_ear = calculate_ear(left_eye_points)
    right_ear = calculate_ear(right_eye_points)
    avg_ear = (left_ear + right_ear) / 2.0

    # EAR threshold for sleep detection (adjustable)
    EAR_THRESHOLD = 0.25

    if avg_ear < EAR_THRESHOLD:
        return "sleeping"
    else:
        return "awake"


app = FastAPI(debug=True)

origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected for sleep detection")
    try:
        while True:
            # Receive base64 encoded frame from frontend
            data = await websocket.receive_text()
            try:
                # Parse JSON data
                frame_data = json.loads(data)
                if frame_data.get("type") == "frame":
                    # Decode base64 image
                    img_data = base64.b64decode(frame_data["data"])
                    np_arr = np.frombuffer(img_data, np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                    if frame is not None:
                        # Detect sleep status
                        status = detect_sleep_status(frame)

                        # Send status back to frontend
                        response = {
                            "type": "status",
                            "status": status,
                            "ear": 0.0  # Could send actual EAR value if needed
                        }
                        await websocket.send_text(json.dumps(response))

                        # Trigger alarm if sleeping (placeholder for audio)
                        if status == "sleeping":
                            print("ALERT: Driver sleeping detected!")
                    else:
                        await websocket.send_text(json.dumps({"type": "error", "message": "Invalid frame"}))
                else:
                    await websocket.send_text(json.dumps({"type": "error", "message": "Unknown message type"}))
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"type": "error", "message": "Invalid JSON"}))
            except Exception as e:
                print(f"Error processing frame: {e}")
                await websocket.send_text(json.dumps({"type": "error", "message": str(e)}))
    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
