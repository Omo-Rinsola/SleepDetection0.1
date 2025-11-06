# Sleep Detection for Drivers

This project is designed to **help prevent road accidents caused by driver drowsiness**, especially for **Lagos drivers** who often spend long hours in traffic and risk feeling sleepy behind the wheel.

The system continuously monitors the driver's eyes using a webcam feed. By applying **computer vision techniques**, it can detect when the driver starts to close their eyes for too long, a key sign of drowsiness, and then **triggers an alarm** to alert the driver before an accident happens.

---

## Features

- **Real-time Video Processing**: Captures and analyzes webcam feed at 10 FPS
- **WebSocket Communication**: Bidirectional communication between frontend and backend
- **Computer Vision Detection**: Uses MediaPipe Face Mesh for accurate facial landmark detection
- **Eye Aspect Ratio (EAR) Analysis**: Calculates EAR to determine drowsiness levels
- **Responsive UI**: Modern Next.js frontend with real-time status updates
- **Cross-platform**: Works on Windows, macOS, and Linux

---

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with WebSocket support
- **Computer Vision**: OpenCV + MediaPipe for face and eye detection
- **Real-time Processing**: Processes video frames and sends status updates
- **CORS Enabled**: Allows frontend communication

### Frontend (Next.js)
- **Framework**: Next.js 14 with TypeScript
- **UI Components**: Shadcn/ui for modern interface
- **Real-time Updates**: WebSocket integration for live status
- **Video Capture**: HTML5 Canvas for frame extraction

---

## How It Works

- **OpenCV** → captures and processes real-time video from the webcam
- **MediaPipe Face Mesh** → detects facial landmarks with high accuracy
- **Eye Aspect Ratio (EAR) logic** → calculates the ratio between eye landmarks to determine if the eyes are closing
- **WebSocket Streaming** → sends video frames from frontend to backend for processing
- **Alarm System** → sounds an alert when EAR values suggest drowsiness

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Webcam access

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Running the Application
1. Start the backend server (runs on http://localhost:8000)
2. Start the frontend server (runs on http://localhost:3000)
3. Open http://localhost:3000 in your browser
4. Click "Start Camera" to begin monitoring

---

## API Endpoints

### WebSocket
- `ws://localhost:8000/ws` - Real-time sleep detection endpoint

**Message Format:**
```json
// Frontend → Backend
{
  "type": "frame",
  "data": "base64-encoded-jpeg"
}

// Backend → Frontend
{
  "type": "status",
  "status": "awake|sleeping|no-face-detected",
  "ear": 0.0
}
```

---

## Configuration

### EAR Threshold
Adjust the sleep detection sensitivity in `backend/main.py`:
```python
EAR_THRESHOLD = 0.25  # Lower = more sensitive
```

### Video Settings
Modify capture settings in `frontend/app/page.tsx`:
```javascript
const captureInterval = 100; // ms (10 FPS)
const quality = 0.8; // JPEG quality
```

---

## Why This Matters

Road safety is a huge concern, especially in places like Lagos where drivers endure long commutes. This project aims to **reduce accidents caused by fatigue** and promote safer driving by providing a **simple yet effective early warning system**.

---

## Technologies Used

- **Backend**: FastAPI, OpenCV, MediaPipe, NumPy
- **Frontend**: Next.js, TypeScript, Tailwind CSS, Shadcn/ui
- **Communication**: WebSockets
- **Computer Vision**: Face detection, landmark tracking, EAR calculation

---

## Future Enhancements

- Audio alarm system integration
- Mobile app version
- Cloud deployment
- Advanced drowsiness detection algorithms
- Integration with vehicle systems
