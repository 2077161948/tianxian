from django.shortcuts import render, redirect
from django.core.files import File
import os


# def upload_view(request):
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # 获取上传的文件对象
#             image = request.FILES['image']
#             # 创建一个文件对象
#             filename = File(open(image.name, 'rb'), name=image.name)
#             # 保存文件到服务器
#             with open(os.path.join('uploads/', filename.name), 'wb') as f:
#                 f.write(filename.read())
#             return redirect('upload_success')
#     else:
#         form = UploadForm()
#     return render(request, 'upload.html', {'form': form})