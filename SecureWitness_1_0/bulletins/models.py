from django.db import models
from django.contrib.auth.models import User

class Bulletin(models.Model):
    Title = models.CharField(max_length=200)
    Author = models.ForeignKey(User) #    (max_length=30)
    Date = models.DateTimeField(auto_now_add=True)  # is Date, Month, Year.  (2002, 12, 31)
    Location = models.TextField()
    Description = models.TextField()    #File_Field = models.FileField(upload_to='documents/secureWitness/uploads/')  #where do I specify the location, is it here?
    #File_Field = models.FileField()  #^ Can specify file path as above or use the path from settings.  Maybe pass variables here for AuthorID
    #pass variables for the username or authorID which will create the directory or path to the right directory?
    #File_Field = models.FileField(upload_to='documents/SecureWitness_1_0/uploads/')  #where do I specify the location, is it here?

    def __unicode__(self):
        return "%s - %s" % (self.Author, self.Title)

    class Meta:
        verbose_name_plural = 'bulletins'