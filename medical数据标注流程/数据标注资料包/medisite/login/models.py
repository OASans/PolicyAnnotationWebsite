#!/usr/bin/env python
# coding=utf-8
from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class User(models.Model):
    id = models.AutoField(verbose_name='用户序号',unique=True,primary_key=True)
    name = models.CharField(verbose_name='用户名',max_length=128)
    password = models.CharField(verbose_name='用户密码',max_length=256)
    start = models.IntegerField(verbose_name='开始序号')
    end = models.IntegerField(verbose_name='结束序号')

    def __str__(self):
        return self.name


class LabelClass(models.Model):
    labelid = models.CharField(verbose_name='BIO类别', unique=True,primary_key=True, max_length=10)
    labelmeaning = models.TextField(verbose_name='BIO含义')

    def __str__(self):
        return str(self.labelid)


class ActClass(models.Model):
    aid = models.CharField(verbose_name='类别id',unique=True,primary_key=True, max_length=10)
    actid = models.TextField(verbose_name='文本类别')

    def __str__(self):
        return self.actid


class PolicyTagger(models.Model):
    id = models.AutoField(verbose_name='用户序号',unique=True,primary_key=True)
    name = models.CharField(verbose_name='用户名',max_length=128)
    password = models.CharField(verbose_name='用户密码',max_length=256)
    start = models.IntegerField(verbose_name='政策开始序号')
    end = models.IntegerField(verbose_name='政策结束序号')

    def __str__(self):
        return self.name


class PolicyText(models.Model):
    example_id = models.IntegerField(verbose_name='政策序号')
    text = models.JSONField(verbose_name='政策原文', null=True, default=[])

    def __str__(self):
        return str(self.example_id)


class PolicySentence(models.Model):
    unique_id = models.CharField(verbose_name='政策句子序号', max_length=20, unique=True, primary_key=True)
    example_id = models.IntegerField(verbose_name='政策序号')
    sentence_id = models.IntegerField(verbose_name='句子序号')

    sentence = models.TextField(verbose_name='句子文本', null=True)

    def __str__(self):
        return self.sentence


class PolicySentenceTag(models.Model):
    id = models.AutoField(verbose_name='记录序号', unique=True, primary_key=True)
    example_id = models.IntegerField(verbose_name='政策序号')
    unique_id = models.CharField(verbose_name='政策句子序号', max_length=20, unique=True)
    sentence_id = models.IntegerField(verbose_name='句子序号')

    sentence = models.TextField(verbose_name='句子文本', null=True)

    sentence_tag = models.CharField(verbose_name='句子类别', max_length=128, default='其他', null=True)
    label = models.CharField(verbose_name='BIO标签', max_length=300,null=True)

    permissions = models.JSONField(verbose_name='准入条件', null=True)

    reviewer = models.IntegerField(verbose_name='标注者id')
    savedate = models.DateTimeField('保存日期', auto_now=True)

    def __str__(self):
        return self.label


class RawText(models.Model):
    unique_id = models.CharField(verbose_name='样本句子序号',max_length=20,unique=True,primary_key=True)
    example_id = models.IntegerField(verbose_name='样本序号')
    sentence_id = models.IntegerField(verbose_name='句子序号')
    speaker = models.TextField(verbose_name='对话人')
    sentence = models.TextField(verbose_name='对话文本',null=True)

    label = models.CharField(verbose_name='预设标签',max_length=300,null=True)
    normalized = models.CharField(verbose_name='归一化症状标签',max_length=128,null=True)
    type = models.CharField(verbose_name='症状判断',max_length=128,null=True)
    drug_word = models.CharField(verbose_name='药品判断',max_length=128,null=True)
    drug_pos = models.CharField(verbose_name='药品位置',max_length=128,null=True)
    check_word = models.CharField(verbose_name='检查判断',max_length=128,null=True)
    check_pos = models.CharField(verbose_name='检查位置',max_length=128,null=True)

    def __str__(self):
        return self.sentence


class SelfReport(models.Model):
    example_id = models.IntegerField(verbose_name='样本序号',unique=True,primary_key=True)
    question = models.TextField(verbose_name='咨询问题')
    diagnose = models.TextField(verbose_name='诊断结果')

    def __str__(self):
        return self.diagnose


class TagText(models.Model):
    id = models.AutoField(verbose_name='记录序号', unique=True, primary_key=True)
    example_id = models.IntegerField(verbose_name='样本序号')
    unique_id = models.CharField(verbose_name='样本句子序号',max_length=128)
    sentence_id = models.IntegerField(verbose_name='句子序号')
    speaker = models.TextField(verbose_name='对话人')
    sentence = models.TextField(verbose_name='对话文本',null=True)
    label = models.CharField(verbose_name='标签', max_length=300,null=True)
    normalized = models.CharField(verbose_name='所有归一化标签', max_length=128,null=True)
    type = models.CharField(verbose_name='所有归一化标签特征', max_length=128,null=True)
    dialogue_act = models.CharField(verbose_name='话语行为', max_length=128,default='其他',null=True)
    report = models.TextField(verbose_name='诊断报告',null=True)
    reviewer = models.IntegerField(verbose_name='用户id')
    savedate = models.DateTimeField('保存日期', default=timezone.now)

    def __str__(self):
        return self.label


