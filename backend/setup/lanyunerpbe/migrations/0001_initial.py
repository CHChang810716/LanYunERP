# Generated by Django 4.0.3 on 2022-03-14 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activated', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstrGroup',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lanyunerpbe.object')),
                ('name', models.CharField(max_length=128)),
            ],
            bases=('lanyunerpbe.object',),
        ),
        migrations.CreateModel(
            name='ManageGroup',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lanyunerpbe.object')),
                ('name', models.CharField(max_length=128)),
            ],
            bases=('lanyunerpbe.object',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lanyunerpbe.object')),
                ('sn', models.CharField(max_length=128)),
                ('sArYear', models.IntegerField(default=1911)),
            ],
            bases=('lanyunerpbe.object',),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lanyunerpbe.object')),
                ('name', models.CharField(max_length=256)),
                ('serialNum', models.CharField(max_length=2048)),
                ('borrowedBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='lanyunerpbe.person')),
                ('igroup', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lanyunerpbe.instrgroup')),
                ('mgroup', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lanyunerpbe.managegroup')),
            ],
            bases=('lanyunerpbe.object',),
        ),
    ]
