# Generated by Django 4.0.10 on 2023-06-25 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_id_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='file',
            field=models.FileField(blank=True, upload_to='files/'),
        ),
    ]
