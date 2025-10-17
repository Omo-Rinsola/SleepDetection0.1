# Changelog

## [Unreleased] - YYYY-MM-DD

### Added
- WebSocket integration for real-time sleep detection between frontend and backend.
- Backend processing of video frames using OpenCV and MediaPipe for Eye Aspect Ratio (EAR) calculation.
- Frontend capture and transmission of video frames via WebSocket.
- Dependencies: opencv-python, mediapipe, numpy added to backend/requirements.txt.

### Changed
- Updated backend/main.py to handle video frame reception, EAR computation, and sleep status broadcasting.
- Updated frontend/app/page.tsx to send video frames and update sleep status based on backend responses, replacing random simulation.

### Technical Details
- Backend now processes incoming base64-encoded video frames, detects faces and eyes using MediaPipe, calculates EAR, and determines sleep status (awake/sleeping/no-face-detected).
- Frontend captures frames from the video stream at intervals, encodes them, and sends via WebSocket; receives and displays real-time status updates.
- Alarm system integration: Backend can trigger alerts when sleeping is detected (placeholder for future audio implementation).

This update transforms the project from a simulated sleep detection to a fully functional real-time system using computer vision.
