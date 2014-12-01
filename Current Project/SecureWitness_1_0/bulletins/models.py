from django.db import models
import operator
from django.db.models import Q
from django.contrib.auth.models import User

#class Permission(models.Model):
    #UserID = models.ForeignKey(User)
    #EncryptedBulletinID = models.ForeignKey(Bulletin)

class BulletinSearch(models.Manager):
    def search(self, search_terms, search_category):
        terms = [term.strip() for term in search_terms.split()]
        q_objects = []
        for term in terms:
            if search_category=='title':
                q_objects.append(Q(Title__icontains=term))
            elif search_category=='pseudonym':
                q_objects.append(Q(Pseudonym__icontains=term))
            elif search_category=='location':
                q_objects.append(Q(Location__icontains=term))
            else:
                q_objects.append(Q(Description__icontains=term))
        qs = self.get_query_set()
        return qs.filter(reduce(operator.or_, q_objects))

class Folder(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    root = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.name

class Bulletin(models.Model):
    folder = models.ForeignKey(Folder)
    objects = BulletinSearch()
    Title = models.CharField(max_length=200)
    Author = models.ForeignKey(User)
    Pseudonym = models.CharField(default='anonymous', max_length=200)
    Date = models.DateTimeField(auto_now_add=True)
    Location = models.TextField()
    Description = models.TextField()
    #Permissions = models.ForeignKey(Permission)
    #path = 'authors/%s/uploads/' % id
    #File_Field = models.FileField(upload_to='uploads/%Y/%m/%d')

    def __unicode__(self):
        return "%s - %s" % (self.Author, self.Title)

    class Meta:
        verbose_name_plural = 'bulletins'

class File(models.Model):
    bulletin = models.ForeignKey(Bulletin)
    File_Field = models.FileField(upload_to='uploads/')
    Is_Encrypted = models.BooleanField(default=True)

    def __unicode__(self):
        return self.File_Field.name

class Permission(models.Model):
    UserID = models.ForeignKey(User)
    FileID = models.ForeignKey(File)