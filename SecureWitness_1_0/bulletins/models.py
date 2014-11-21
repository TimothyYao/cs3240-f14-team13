from django.db import models
from django.contrib.auth.models import User

#class Permission(models.Model):
    #UserID = models.ForeignKey(User)
    #EncryptedBulletinID = models.ForeignKey(Bulletin)

class Bulletin(models.Model):
    Title = models.CharField(max_length=200)
    Author = models.ForeignKey(User)
    Date = models.DateTimeField(auto_now_add=True)
    Location = models.TextField()
    Description = models.TextField()
    #Permissions = models.ForeignKey(Permission)
    #filepath = 'authors/%s/uploads/' % (Bulletin.id)
    #File_Field = models.FileField(upload_to=filepath)

    def __unicode__(self):
        return "%s - %s" % (self.Author, self.Title)

    class Meta:
        verbose_name_plural = 'bulletins'