from django.db import models


# Create your models here.
class file_model:

    def __init__(self):
        self.image_file_buff = None
        self.image_file_list = []
        self.video_file_buff = None
        self.video_file_list = []
        self.txt = ''
        self.txt_list = []
        self.type = 0
