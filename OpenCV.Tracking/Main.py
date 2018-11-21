from Camera import CameraCapture

if __name__ == "__main__":    
    # Create camera capture and start preview
    camera_capture = CameraCapture()    
    camera_capture.start_preview()

    # Release resources
    camera_capture.release()
    
