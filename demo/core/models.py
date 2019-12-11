from django.db import models
from users.models import MainUser

from core.constants import TASK_STATUSES, TASK_TODO, TASK_DONE, TASK_PRIORITIES, TASK_PRIORITY_MEDIUM
from utils.upload import task_document_path
from utils.validators import validate_extension, validate_file_size


class Project(models.Model):
    name = models.CharField(max_length=300)
    desc = models.TextField()
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='projects')

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name

    @property
    def tasks_count(self):
        return self.tasks.count()


class TaskDoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TASK_DONE)

    def done_tasks(self):
        return self.filter(status=TASK_DONE)

    def filter_by_status(self, status):
        return self.filter(status=status)


class TaskTodoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TASK_TODO)

    def filter_by_status(self, status):
        return self.filter(status=status)


class Task(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=TASK_STATUSES, default=TASK_TODO)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='tasks', null=True)
    document = models.FileField(upload_to=task_document_path, validators=[validate_file_size, validate_extension],
                                blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(default='')
    priority = models.PositiveIntegerField(choices=TASK_PRIORITIES, default=TASK_PRIORITY_MEDIUM)
    executor = models.ForeignKey(MainUser, on_delete=models.SET_NULL, related_name='my_tasks', null=True)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='created_tasks')

    objects = models.Manager()
    done_tasks = TaskDoneManager()
    todo_tasks = TaskTodoManager()

    class Meta:
        unique_together = ('project', 'name')
        ordering = ('name', 'status',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        db_table = 'my_tasks'

    def __str__(self):
        return self.name

    def set_executor(self, executor_id):
        self.executor_id = executor_id
        self.save()
