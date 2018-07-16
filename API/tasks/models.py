from django.db import models


class Task(models.Model):

    name = models.CharField(max_length=80)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    start = models.DateTimeField(db_index=True)
    finished = models.DateTimeField(null=True, blank=True)

    content = models.TextField(max_length=1000)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Task'
