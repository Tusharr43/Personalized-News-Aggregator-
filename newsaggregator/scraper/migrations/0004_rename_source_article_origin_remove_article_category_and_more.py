# Generated by Django 5.1.1 on 2024-09-13 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_alter_article_category_alter_article_summary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='source',
            new_name='origin',
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='publication_date',
        ),
        migrations.AddField(
            model_name='article',
            name='date',
            field=models.DateField(default='2024-01-01'),
        ),
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.TextField(default='2024-01-01'),
            preserve_default=False,
        ),
    ]
