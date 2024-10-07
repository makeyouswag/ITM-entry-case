from django.db import models

class Task(models.Model):
    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True)
    state = models.CharField(
        max_length=200
    )
    groups = models.ManyToManyField("Group", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['title']


class Group(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=200)
    description = models.TextField(verbose_name="Описание", blank=True)