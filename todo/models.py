from django.db import models


class Todo(models.Model):
    class YearInSchool(models.TextChoices):
        TODO = 'todo'
        IN_PROGRESS = 'in_progress'
        COMPLETED = 'completed'
    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True)
    state = models.CharField(
        max_length=200,
        choices=YearInSchool.choices
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
