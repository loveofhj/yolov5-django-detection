import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from .models import load_model
import shutil

# YOLOv5 모델 로드
try:
    model = load_model()
except FileNotFoundError as e:
    print(f"Error loading YOLOv5 model: {e}")
    model = None

def detect(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        if not image:
            return JsonResponse({'status': 'error', 'message': 'No image uploaded'})

        # 저장할 파일명 생성
        file_name = f"{uuid.uuid4()}.jpg"
        save_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # 이미지 저장
        with open(save_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # 모델이 로드되지 않은 경우
        if model is None:
            return JsonResponse({'status': 'error', 'message': 'Model not loaded'})

        # 결과 이미지 저장 경로 설정
        result_dir = os.path.join(settings.MEDIA_ROOT, "results")
        os.makedirs(result_dir, exist_ok=True)

        # YOLOv5 결과 저장 경로
        output_file_name = f"{file_name}"
        output_path = os.path.join(result_dir, output_file_name)

        # YOLOv5 모델 예측
        results = model(save_path)
        results.save()  # 기본적으로 runs/detect/exp에 저장됨

        # YOLOv5의 기본 저장 경로
        exp_dir = os.path.join(settings.BASE_DIR, "runs", "detect", "exp")

        # exp2, exp3 등 폴더가 생성될 수 있으므로, 모든 exp 폴더를 탐색
        runs_dir = os.path.join(settings.BASE_DIR, "runs", "detect")
        if os.path.exists(runs_dir):
            for folder in os.listdir(runs_dir):
                folder_path = os.path.join(runs_dir, folder)

                # exp 폴더 내의 파일을 모두 이동
                if os.path.isdir(folder_path):
                    for file_name in os.listdir(folder_path):
                        src_path = os.path.join(folder_path, file_name)
                        dest_path = os.path.join(result_dir, file_name)

                        # 파일이 이미 존재하면 덮어쓰기
                        if os.path.exists(dest_path):
                            os.remove(dest_path)

                        shutil.move(src_path, dest_path)

                    # exp 폴더 삭제
                    shutil.rmtree(folder_path)

        # 결과 이미지 URL 경로
        output_file_url = f"{settings.MEDIA_URL}results/{output_file_name}"
        print(f"Final saved path: {output_file_url}")

        

        return JsonResponse({
            'status': 'success',
            'message': 'Object detection completed',
            'file_url': output_file_url,
        })

    return render(request, 'detection/detect.html')
