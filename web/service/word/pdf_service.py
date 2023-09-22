import os
import uuid
import zipfile

import PyPDF2
from docx import Document
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfquery import PDFQuery
from pdf2docx import parse, Converter
from docx2pdf import convert
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from io import StringIO
import pdfminer.high_level
import pdfminer.layout

from tianxian.settings import MEDIA_ROOT
from web.util.file_util import upload_file, result_file


class PdfService:
    pdf_data = []

    def __init__(self,request):
        self.request = request

        # if len(pdf_list) > 1:
        #     for page in range(pdfReader.numPages):
        #         pdfWriter.addPage(pdfReader.getPage(page))
        #     pdfFileObj.close()

    def encryption_pdf(self,password):
        ###
        # 加密pdf文件
        # path 加密数据
        # password 密码
        ###
        file_list = upload_file(self.request)
        for item in file_list:
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.encrypt(password)
            pdf_file = open(item['path'], 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for page in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page))
            pdf_out_file = open(item['path'], 'wb')
            pdf_writer.write(pdf_out_file)
            pdf_file.close()
            pdf_out_file.close()
        return result_file(file_list)

    # def colse_pdf(self):
    #     if type(self.pdf_data) is str:
    #         self.pdf_data.
    def text_pdf(self):
        file_list = upload_file(self.request)
        result = []
        for item in file_list:
            resource_manager = PDFResourceManager()
            fake_file_handle = StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams(),codec='utf-8')
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            with open(item['path'], 'rb') as fh:
                for page in PDFPage.get_pages(fh, set()):
                    page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
            converter.close()
            fake_file_handle.close()
            result.append(text)
            return result

    def pdf_to_world(self):
        file_list = upload_file(self.request)
        result_file_path = []
        for item in file_list:
            data = {}
            name = f'{uuid.uuid4()}.docx'
            word_file = os.path.join(MEDIA_ROOT, name)
            fp = open(item['path'], 'rb')
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed
            else:
                out = Document()
                rsrcmagr = PDFResourceManager()
                laparams = LAParams()
                device = PDFPageAggregator(rsrcmagr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmagr, device)
                for page in PDFPage.create_pages(doc):
                    interpreter.process_page(page)
                    layout = device.get_result()
                    for x in layout:
                        print(x)
                        pass
            #parse(pdf_file=item['path'],docx_file=word_file)
            # convert pdf to docx
            cv = Converter(item['path'])
            cv.convert(word_file)  # 默认参数start=0, end=None
            cv.close()
            data['path'] = word_file
            data['name'] = name
            result_file_path.append(data)
        return result_file(result_file_path)
