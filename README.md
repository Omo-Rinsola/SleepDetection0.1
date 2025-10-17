# Sleep Detection for Drivers  

This project is designed to **help prevent road accidents caused by driver drowsiness**, especially for **Lagos drivers** who often spend long hours in traffic and risk feeling sleepy behind the wheel.  

The system continuously monitors the driver’s eyes using a webcam feed. By applying **computer vision techniques**, it can detect when the driver starts to close their eyes for too long , a key sign of drowsiness  and then **triggers an alarm** to alert the driver before an accident happens.  

---

##  How it Works  

- **OpenCV** → captures and processes real-time video from the webcam  
- **MediaPipe Face Mesh** → detects facial landmarks with high accuracy  
- **Eye Aspect Ratio (EAR) logic** → calculates the ratio between eye landmarks to determine if the eyes are closing  
- **Alarm System** → sounds an alert when EAR values suggest drowsiness  

---

##  Why this Matters  

Road safety is a huge concern, especially in places like Lagos where drivers endure long commutes. This project aims to **reduce accidents caused by fatigue** and promote safer driving by providing a **simple yet effective early warning system**.  
