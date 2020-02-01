from django.db import models
from django.utils import timezone

class User(models.Model):
    email=models.CharField(
    verbose_name='メールアドレス',
    max_length=255,
    unique=True,
    )
    password=models.CharField(
    verbose_name='パスワード',
    max_length=8,
    )
    last_login=models.DateTimeField(
    verbose_name='ログイン日時',
    default=timezone.now
    )

class Diary(models.Model):
    email=models.CharField(
    verbose_name='メールアドレス',
    max_length=255,
    )
    diary=models.CharField(
    verbose_name='日記',
    max_length=500,
    )
    positive=models.FloatField(
    verbose_name='ポジティブ',
    default=0,
    )
    negative=models.FloatField(
    verbose_name='ネガティブ',
    )
    default=0,
    created_at=models.DateTimeField(
    verbose_name='投稿日',
    default=timezone.now
    )

class WordDict(models.Model):
    word=models.CharField(
    verbose_name='ワード',
    max_length=255,
    unique=True
    )
    negaposi=models.FloatField(
    verbose_name='ネガポジ',
    default=0
    )
