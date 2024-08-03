from django.db import models

class UploadFile(models.Model):
    title = models.CharField(
        default= '제목 없음',
        max_length=50)
    file = models.ImageField(null = True, upload_to='')
    output = models.TextField(default = '내용 없음', blank=True, null=True)  # 결과를 저장할 필드

    def __str__(self):
        return f"제목:{self.title} 파일명:{self.file} 내용:{self.output}" 