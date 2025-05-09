from django.db import models

# Create your models here.
import torch
import os
from django.conf import settings

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_PATH = os.path.join(BASE_DIR, "yolov5", "yolov5s.pt")

def load_model():
    """
    YOLOv5 모델을 로드하는 함수.
    """
    model_path = os.path.join(settings.BASE_DIR, 'yolov5', 'yolov5s.pt')
    
    # 모델이 존재하는지 확인
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"YOLOv5 모델 파일이 존재하지 않습니다: {model_path}")

    # YOLOv5 모델 로드
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    return model

class Detection(models.Model):
    image = models.ImageField(upload_to='uploads/')
    detected_image = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)