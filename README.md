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

## How It Works (Basic flow)

- Your webcam captures video of your face in real time
- forntend Sends webcam frames to the backend every 50ms 
- MediaPipe detects landmarks around your eyes (like eyelids and corners)  
- The backend calculates the Eye Aspect Ratio (EAR), a simple number that shows how open or closed your eyes are  
- If EAR stays below a threshold for a few frames, the system flags drowsiness  
- The backend sends the status to the frontend over WebSockets  
- The frontend updates the UI and plays an alarm  

---

## Run it locally

### Prerequisites
- Python 3.8+
- Node.js 18+
- Webcam access

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
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

## Try it live 

You can test the app here: [Sleep Detection Live](https://your-live-app-link.comsleep-detection0-1.vercel.app)  

⚠️ Note: Real-time updates currently have noticeable latency. Improvements are planned.

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

## Technologies Used

- **Backend**: FastAPI, OpenCV, MediaPipe, NumPy
- **Frontend**: Next.js, TypeScript, Tailwind CSS, Shadcn/ui
- **Communication**: WebSockets
- **Computer Vision**: Face detection, landmark tracking, EAR calculation

---

## Future Enhancements / Contributions
- Reduce latency for faster real-time updates on the live app
- Mobile app version
- Cloud deployment
- Advanced drowsiness detection algorithms
- Integration with vehicle systems
- improved UI
