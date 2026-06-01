from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_russify_directors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='name',
            field=models.CharField('имя', max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='director',
            name='description',
            field=models.TextField('описание', blank=True),
        ),
        migrations.AlterField(
            model_name='director',
            name='link',
            field=models.URLField('ссылка', blank=True),
        ),
    ]
