from django.db import models
from users.models import User as user
from django.core.exceptions import ValidationError

# Create your models here.
class TODO(models.Model):
    
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=250)
    create_date = models.DateTimeField()
    todo_date = models.DateTimeField()
    done = models.BooleanField(default=False)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def clean(self):
        # jestli je datum a čas do kdy splnit úkol větší nebo rovno datu a času vytvoření
        if self.todo_date < self.create_date:
            raise ValidationError("\"todo_date\" must be bigger or equal to \"create_date\"")