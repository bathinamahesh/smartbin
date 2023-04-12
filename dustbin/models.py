from django.db import models

class dustbinpercent(models.Model):
    dustbin = models.TextField(max_length=10, unique=True)
    percent = models.TextField(max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = ("Dustbin name")
        verbose_name_plural = ("Assignmentss")

    def __str__(self):
        return str(self.dustbin)+" "+str(self.percent)
