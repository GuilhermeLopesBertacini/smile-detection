# Smile Detection

Real-time smile detection using OpenCV and MediaPipe.

---

## 🧠 Description

This project uses facial landmarks to detect smiles based on the relative position of mouth landmarks. It's designed to run easily inside a Docker container, with optional volume mounting for development.

---

## 📁 Project Structure

```

smile-detection/
├── Dockerfile           # Container configuration
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
└── rt\_detection.py      # Main script for smile detection

````

---

## 🐳 Run with Docker

### 1. Build the container

```bash
docker build -t smile-detection .
````

### 2. Run the detection script with camera access

```bash
docker run --rm -it --device /dev/video0 smile-detection
```

### 3. Run with live code volume and display (Linux)

```bash
xhost +local:root  # Allow local root access to X11

docker run --rm -it \
  --device /dev/video0 \
  -v "$(pwd)":/app \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  smile-detection
```

> This allows you to edit the code on your machine and see the changes without rebuilding the image.

### 4. Open a terminal inside the container

```bash
docker run --rm -it smile-detection /bin/bash
```

---

## 📝 Notes

* Make sure your webcam is accessible as `/dev/video0`.
* X11 forwarding is required to display the OpenCV window when using volume mapping.
* Adjust smile detection thresholds inside `rt_detection.py` for better accuracy depending on lighting, camera quality, and distance.

---

## 🔧 Dependencies

All Python dependencies are listed in `requirements.txt`. These are automatically installed inside the Docker container.
