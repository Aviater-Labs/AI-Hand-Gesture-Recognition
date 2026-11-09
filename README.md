# AI-Based Hand Gesture Recognition System

A Python-based computer vision application that detects hand landmarks through a webcam and recognises three predefined gestures: PEACE, STOP and CHILL.

## Features

- Real-time webcam input using OpenCV.
- Hand landmark detection using MediaPipe.
- Recognition of three predefined hand gestures.
- Gesture stability filtering.
- Automatic download of the required hand landmark model.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Requests

## Recognised Gestures

| Gesture | Description |
|---|---|
| PEACE | Index and middle fingers extended |
| STOP | All five fingers extended |
| CHILL | Thumb and little finger extended |

## Installation

1. Install Python.
2. Download or clone this repository.
3. Run `Install.bat` to install the required libraries.
4. Execute the application:

```bash
python program.py
```

Press `Q` to close the application.

## Project Structure

```text
AI-Hand-Gesture-Recognition/
├── program.py
├── Install.bat
├── README.md
└── screenshots/
    ├── peace.png
    ├── stop.png
    └── chill.png
```

## Working Principle

MediaPipe detects 21 hand landmarks. The Python program analyses their coordinates using predefined logical conditions to classify the detected gesture.

The project uses a pre-trained hand landmark detection model and rule-based gesture classification.

## Limitations

- Currently supports three predefined gestures.
- Detection depends on lighting and camera positioning.
- Gesture recognition works best with the palm facing the camera.
