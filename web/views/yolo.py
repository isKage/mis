from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import torch
import cv2
import os


def index(request):
    return render(request, 'yolo_index.html')


def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        # 保存上传的文件
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # 使用 YOLO 模型加载并检测
        # torch.hub.set_dir('../../utils/cache')
        model = torch.hub.load(
            '/Users/shukunjun/Desktop/code/django/mis/cache/ultralytics_yolov5_master',
            'custom',
            path='/Users/shukunjun/Desktop/code/django/mis/yolov5s.pt',
            source='local',
        )

        img_path = fs.path(filename)
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 进行 YOLO 检测
        results = model(img_rgb)

        # 提取检测结果并绘制标记
        detections = results.pandas().xyxy[0]  # 获取 DataFrame
        people_detections = detections[detections['name'] == 'person']
        count = len(people_detections)

        # 在图像上绘制边界框
        save_dir = 'media/processed'
        results.save(save_dir=save_dir)  # 保存到 'media/processed' 目录

        # 动态获取生成的文件名
        output_files = os.listdir(save_dir)
        output_files = [f for f in output_files if f.endswith('.jpg') or f.endswith('.png')]
        if output_files:
            processed_image_path = f'/media/processed/{output_files[-1]}'  # 获取最新的文件
        else:
            processed_image_path = None

        count = len(results.pandas().xyxy[0][results.pandas().xyxy[0]['name'] == 'person'])  # 获取检测到的人员数

        return render(request, 'yolo_index.html', {
            'image_url': processed_image_path,
            'count': count
        })

        # processed_image_path = f'/media/processed/{filename}'
        #
        # return render(request, 'yolo_index.html', {
        #     'image_url': processed_image_path,
        #     'count': count
        # })

    return render(request, 'yolo_index.html')