# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-30 22:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Academic',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appraisal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('deadline', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Competency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('technical', 'Technical competency'), ('social', 'Social competency'), ('personal', 'Personal competency')], default='technical', max_length=16)),
            ],
            options={
                'verbose_name_plural': 'competencies',
            },
        ),
        migrations.CreateModel(
            name='CompetencyEndorsement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('progress', models.CharField(choices=[('0', 'none'), ('1', 'basic'), ('2', 'good'), ('3', 'excellent')], max_length=16)),
            ],
            options={
                'verbose_name_plural': 'competency endorsements',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('year', models.CharField(blank=True, choices=[('0', 'mixed year'), ('1', 'first year'), ('2', 'second year'), ('3', 'third year'), ('4', 'fourth year'), ('5', 'postgraduate')], max_length=8, null=True)),
                ('moodle', models.URLField(blank=True, null=True)),
                ('ILOs', models.TextField(blank=True, null=True)),
                ('missed_lecture_procedure', models.TextField(blank=True, null=True)),
                ('lecture_recordings', models.URLField(blank=True, max_length=300, null=True)),
                ('slug', models.SlugField()),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='interactWBL.Academic')),
            ],
        ),
        migrations.CreateModel(
            name='CourseTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Competency')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Course')),
            ],
            options={
                'verbose_name_plural': 'Course targets',
            },
        ),
        migrations.CreateModel(
            name='Enrolment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Company')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalCompetency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.CharField(choices=[('0', 'none'), ('1', 'basic'), ('2', 'good'), ('3', 'excellent')], default='0', max_length=16)),
                ('assignments', models.ManyToManyField(blank=True, to='interactWBL.Assignment')),
                ('competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Competency')),
            ],
            options={
                'verbose_name_plural': 'personal competencies',
            },
        ),
        migrations.CreateModel(
            name='Reflection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('quick', 'Quick Reflection'), ('weekly', 'Weekly Reflection')], max_length=32)),
                ('date', models.DateField(auto_now_add=True)),
                ('content', models.TextField()),
                ('assignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Assignment')),
                ('competencies', models.ManyToManyField(to='interactWBL.Competency')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('year', models.CharField(choices=[('1', 'first year'), ('2', 'second year'), ('3', 'third year'), ('4', 'fourth year'), ('5', 'postgraduate')], default=1, max_length=8)),
                ('competencies_in_focus', models.ManyToManyField(blank=True, to='interactWBL.Competency')),
                ('mentor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='interactWBL.Mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True, max_length=1000)),
                ('grade', models.CharField(default='not graded', max_length=16)),
                ('file', models.FileField(upload_to='coursework_submissions')),
                ('date', models.DateField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Assignment')),
                ('grader', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Academic')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Student')),
            ],
        ),
        migrations.AddField(
            model_name='reflection',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Student'),
        ),
        migrations.AddField(
            model_name='personalcompetency',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Student'),
        ),
        migrations.AddField(
            model_name='enrolment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Student'),
        ),
        migrations.AddField(
            model_name='competencyendorsement',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='competencyendorsement',
            name='competency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.PersonalCompetency'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='competencies',
            field=models.ManyToManyField(to='interactWBL.Competency'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Mentor'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Student'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Mentor'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactWBL.Student'),
        ),
    ]
