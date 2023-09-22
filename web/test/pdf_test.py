import io
import re

import pdfplumber

import fitz
import docx
import PyPDF2
from PyPDF2 import PdfReader

import PyPDF2
import fitz

import PyPDF2
import fitz


def extract_image_info(pdf_path):
    # 使用 PyMuPDF 打开 PDF 文件
    doc = fitz.open(pdf_path)

    for page_number in range(doc.page_count):
        # 加载每一页
        page = doc.load_page(page_number)

        # 获取页面上的图像块
        image_blocks = page.get_images(full=True)

        for i, block in enumerate(image_blocks):
            x, y, x1, y1 = block[0:4]  # 获取图像块边界的左下角和右上角坐标
            width = x1 - x  # 计算宽度
            height = y1 - y  # 计算高度

            image_size = (width,height)

            print(f"第 {page_number + 1} 页，图像块 {i + 1}")
            print("位置信息：x =", x, ", y =", y, ", 宽度 =", width, ", 高度 =", height)
            print("大小信息：宽度 =", image_size[0], ", 高度 =", image_size[1])

    doc.close()

# 指定要操作的 PDF 文件路径
pdf_file = "/Users/huangfeilong/Documents/code/python/tianxian/img/2077/1/manual_es.pdf"

# 调用函数提取图像的大小和位置信息
extract_image_info(pdf_file)
