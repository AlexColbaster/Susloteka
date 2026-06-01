from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0010_review_constraints'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
            ],
            options={
                'db_table': 'logs',
                'ordering': ['-date'],
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
    ]
