# Generated by Django 4.2.5 on 2023-09-13 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TiffFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(upload_to='uploads/')),
                ('dzi_file', models.FilePathField(blank=True, null=True)),
            ],
        ),
    ]
