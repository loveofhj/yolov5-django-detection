# YOLOv5 Django Object Detection App

A simple web application that integrates YOLOv5 for real-time object detection using Django.

## Installation

1. Clone the repository:
git clone --recurse-submodules https://github.com/yourusername/yolov5-django-app.git
cd yolov5-django-app

2. Create and activate a virtual environment:
python -m venv yolov5_django_env
source yolov5_django_env/bin/activate  # Windows: .\yolov5_django_env\Scripts\activate
## 패키지 설치
pip install django

pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

pip install opencv-python-headless

pip install pillow numpy matplotlib requests


3. Install dependencies:
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt

4. Download the YOLOv5 model weights:
cd yolov5
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt -O models/yolov5s.pt

