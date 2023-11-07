from django.shortcuts import render
from django.http import HttpResponse

from pdf2docx import Converter

import os


# Create your views here.

def index(request):
    # return redirect("index:shop",permanent=True)
    return render(request, "index.html")


def upload(request):
    # 请求方法为POST时，执行文件上传
    print("debug ++++++++++++++++++++++++")
    print(request.method)
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，就默认为None
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return HttpResponse("no files for upload")
        # 打开特定的文件进行二进制的写操作
        f = open(os.path.join("./", myFile.name), "wb+")
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()

        docx_file = './parsed.docx'
        source_file = os.path.join("./", myFile.name)

        cv = Converter(source_file)
        cv.convert(docx_file)  # all pages by default
        cv.close()

        file = open(docx_file, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(docx_file)

        return response
    else:
        # 请求方法为get时，生成文件上传页面
        return render(request, "index.html")
