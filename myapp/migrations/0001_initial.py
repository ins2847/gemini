# Generated by Django 5.0.3 on 2024-08-03 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='제목 없음', max_length=50)),
                ('file', models.ImageField(null=True, upload_to='')),
                ('output', models.TextField(blank=True, default='내용 없음', null=True)),
            ],
        ),
    ]
