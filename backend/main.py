from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from detector import Detect
import uvicorn
import cv2
import json
import numpy as np
import base64



# class Status(BaseModel):
#     status: str = Field(..., description="sleep status detected")
#     average_ear: float = Field(... , description="The average EAR value")

app = FastAPI(debug=True)
detect = Detect()

origins = [
    "http://localhost:3000",
    "https://sleep-detection0-1.vercel.app/",
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
                        status = detect.detect(frame)

                        # send status to frontend
                        response = {
                            "type": "status",
                            "status": status,
                        }
                        await websocket.send_text(json.dumps(response))
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


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
