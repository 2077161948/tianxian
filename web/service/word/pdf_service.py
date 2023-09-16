import PyPDF2
from pdfquery import PDFQuery
from pdf2docx import parse
from docx2pdf import convert


class pdf_service:
    pdf_data = []

    def read_pdf(self, path):
        if type(path) is str:
            pdf_file = open(path, 'rb')
            self.pdf_data = PyPDF2.PdfFileReader(pdf_file)

        elif type(path) is list:
            for item in path:
                pdf_file = open(item, 'rb')
                self.pdf_data.append(PyPDF2.PdfFileReader(pdf_file))

        # if len(pdf_list) > 1:
        #     for page in range(pdfReader.numPages):
        #         pdfWriter.addPage(pdfReader.getPage(page))
        #     pdfFileObj.close()

    def encryption_pdf(self, path, password):
        ###
        # 加密pdf文件
        # path 加密数据
        # password 密码
        ###
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.encrypt(password)
        pdf_file = open(path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page))
        pdf_out_file = open(path, 'wb')
        pdf_writer.write(pdf_out_file)
        pdf_file.close()
        pdf_out_file.close()

    # def colse_pdf(self):
    #     if type(self.pdf_data) is str:
    #         self.pdf_data.
    def text_pdf(self):
        pageTexts = []
        for pageNum in range(self.pdf_data.numPages):
            page = self.pdf_data.getPage(pageNum)
            pageTexts.append(page.extractText())

    def pdf_to_world(self, pdf_file, word_file):
        parse(pdf_file, word_file)
