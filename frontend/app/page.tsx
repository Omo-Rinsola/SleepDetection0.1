"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { Camera, CameraOff } from "lucide-react"

type SleepStatus = "awake" | "sleeping" | "no-face-detected" | "camera-off"

export default function SleepDetectionApp() {
  const [isRecording, setIsRecording] = useState(false)
  const [sleepStatus, setSleepStatus] = useState<SleepStatus>("camera-off")
  const [stream, setStream] = useState<MediaStream | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const websocketRef = useRef(null)
  const videoRef = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    if (isRecording) {
      // Create WebSocket connection
      const socket = new WebSocket("ws://localhost:8000/ws")
      websocketRef.current = socket

      socket.onopen = () => {
        console.log("[WebSocket] Connected to backend ")
        setIsConnected(true)
        // Send test message to confirm
        socket.send("Frontend connected!")
      }

      socket.onmessage = (event) => {
        console.log("[WebSocket] Message from backend:", event.data)
      }

      socket.onclose = () => {
        console.log("[WebSocket] Disconnected ")
        setIsConnected(false)
      }

      socket.onerror = (error) => {
        console.error("[WebSocket] Error:", error)
      }

      // Cleanup when component unmounts or recording stops
      return () => {
        console.log("[WebSocket] Closing connection...")
        socket.close()
      }
    }
  }, [isRecording])


  useEffect(() => {
    if (!isRecording) return

    const statuses: SleepStatus[] = ["awake", "sleeping", "no-face-detected"]
    const interval = setInterval(() => {
      setSleepStatus(statuses[Math.floor(Math.random() * statuses.length)])
    }, 3000)

    return () => clearInterval(interval)
  }, [isRecording])

  const startCamera = async () => {
    try {
      console.log("[v0] Requesting camera access...")

      setIsRecording(true)
      setSleepStatus("awake")

      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: "user",
        },
        audio: false,
      })

      console.log("[v0] Camera stream obtained:", mediaStream)
      console.log("[v0] Video tracks:", mediaStream.getVideoTracks())

      setTimeout(() => {
        if (videoRef.current) {
          console.log("[v0] Setting video srcObject...")
          videoRef.current.srcObject = mediaStream

          videoRef.current.onloadedmetadata = () => {
            console.log("[v0] Video metadata loaded")
          }

          videoRef.current.oncanplay = () => {
            console.log("[v0] Video can play")
          }

          videoRef.current
            .play()
            .then(() => {
              console.log("[v0] Video playing successfully")
            })
            .catch((playError) => {
              console.error("[v0] Error playing video:", playError)
            })
        } else {
          console.error("[v0] Video element still not found in DOM")
          mediaStream.getTracks().forEach((track) => track.stop())
          setIsRecording(false)
          setSleepStatus("camera-off")
          return
        }
      }, 100)

      setStream(mediaStream)
    } catch (error) {
      console.error("[v0] Error accessing camera:", error)
      alert("Could not access camera. Please check permissions.")
      setIsRecording(false)
      setSleepStatus("camera-off")
    }
  }

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop())
      setStream(null)
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null
    }

    setIsRecording(false)
    setSleepStatus("camera-off")
  }




  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop())
      }
    }
  }, [stream])

  const getStatusConfig = (status: SleepStatus) => {
    switch (status) {
      case "awake":
        return { text: "Awake", variant: "default" as const, color: "bg-green-500" }
      case "sleeping":
        return { text: "Sleeping", variant: "secondary" as const, color: "bg-red-500" }
      case "no-face-detected":
        return { text: "No Face Detected", variant: "destructive" as const, color: "bg-yellow-500" }
      case "camera-off":
        return { text: "Camera Off", variant: "outline" as const, color: "bg-gray-500" }
    }
  }

  const statusConfig = getStatusConfig(sleepStatus)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Sleep Detection Monitor</h1>
          <p className="text-slate-600">Real-time sleep status monitoring</p>
        </div>

        {/* Main Video Feed */}
        <Card className="relative mb-8 overflow-hidden bg-slate-900 border-0 shadow-2xl">
          <div className="aspect-video relative">
            {isRecording ? (
              <>
                <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover" />
                {/* Status Overlay */}
                <div className="absolute top-4 left-4">
                  <Badge variant={statusConfig.variant} className="px-4 py-2 text-sm font-medium shadow-lg">
                    <div className={`w-2 h-2 rounded-full ${statusConfig.color} mr-2 animate-pulse`} />
                    {statusConfig.text}
                  </Badge>
                </div>

                {/* Recording Indicator */}
                <div className="absolute top-4 right-4">
                  <Badge variant="destructive" className="px-3 py-1 shadow-lg">
                    <div className="w-2 h-2 rounded-full bg-red-400 mr-2 animate-pulse" />
                    Recording
                  </Badge>
                </div>
              </>
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-slate-800">
                <div className="text-center">
                  <CameraOff className="w-16 h-16 text-slate-400 mx-auto mb-4" />
                  <p className="text-slate-300 text-lg">Camera is off</p>
                  <p className="text-slate-500 text-sm">Click "Start Camera" to begin monitoring</p>
                </div>
              </div>
            )}
          </div>
        </Card>

        {/* Control Buttons */}
        <div className="flex justify-center gap-4 mb-8">
          {!isRecording ? (
            <Button
              onClick={startCamera}
              size="lg"
              className="px-8 py-3 text-lg font-medium bg-green-600 hover:bg-green-700"
            >
              <Camera className="w-5 h-5 mr-2" />
              Start Camera
            </Button>
          ) : (
            <Button onClick={stopCamera} size="lg" variant="destructive" className="px-8 py-3 text-lg font-medium">
              <CameraOff className="w-5 h-5 mr-2" />
              Stop Camera
            </Button>
          )}
        </div>

        {/* Status Information */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-6 text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <div className="w-6 h-6 bg-green-500 rounded-full" />
            </div>
            <h3 className="font-semibold text-slate-800 mb-1">Awake</h3>
            <p className="text-sm text-slate-600">Eyes open and alert</p>
          </Card>

          <Card className="p-6 text-center">
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <div className="w-6 h-6 bg-red-500 rounded-full" />
            </div>
            <h3 className="font-semibold text-slate-800 mb-1">Sleeping</h3>
            <p className="text-sm text-slate-600">Eyes closed, sleeping detected</p>
          </Card>

          <Card className="p-6 text-center">
            <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <div className="w-6 h-6 bg-yellow-500 rounded-full" />
            </div>
            <h3 className="font-semibold text-slate-800 mb-1">No Face</h3>
            <p className="text-sm text-slate-600">Face not detected in frame</p>
          </Card>
        </div>
      </div>
    </div>
  )
}
