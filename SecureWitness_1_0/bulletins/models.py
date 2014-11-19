from django.db import models
from django.contrib.auth.models import User

class Bulletin(models.Model):
    Title = models.CharField(max_length=200)
    Author = models.ForeignKey(User)
    Date = models.DateTimeField(auto_now_add=True)
    Location = models.TextField()
    Description = models.TextField()
    #File_Field = models.FileField(upload_to='documents/SecureWitness_1_0/uploads/')

    def __unicode__(self):
        return "%s - %s" % (self.Author, self.Title)

    class Meta:
        verbose_name_plural = 'bulletins'