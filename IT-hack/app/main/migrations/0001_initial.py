# Generated by Django 5.0.4 on 2024-04-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=150)),
                ('number_of_seats', models.IntegerField(default=100)),
                ('is_solo', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Place_room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_room_id', models.IntegerField(null=True)),
                ('place_room_int', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Place_roomMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pr_id', models.IntegerField()),
                ('user', models.CharField(max_length=150)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PlaceMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_id', models.IntegerField()),
                ('user', models.CharField(max_length=150)),
            ],
        ),
    ]
