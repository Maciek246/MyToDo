from django.db import models


class Task(models.Model):

    name = models.CharField(max_length=80)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    start = models.DateTimeField(db_index=True)
    finished = models.DateTimeField(null=True, blank=True)

    content = models.TextField(max_length=1000, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Task'

    def __str__(self):
        return f"{self.name} {self.start}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.content:
            self.content = self.name
        return super(Task, self).save()
