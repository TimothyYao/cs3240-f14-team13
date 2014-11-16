from django.db import models

# Create your models here.



# TODO fix data types later amd match the form input on html page.
# class Bulletin(models.Model):
#     Author_ID = models.TextField #    (max_length=30)
#     Date = models.DateField()  # is Date, Month, Year.  (2002, 12, 31)
#     Address = models.TextField
#     Post_Code = models.IntegerField(max_length=10) #I think max zip is 10.  "zip+4"
#     Country = models.CharField()
#     Description = models.TextField

class Bulletin(models.Model):
    Author_ID = models.TextField() #    (max_length=30)
    Date = models.TextField()  # is Date, Month, Year.  (2002, 12, 31)
    Address = models.TextField()
    Post_Code = models.TextField() #I think max zip is 10.  "zip+4"
    Country = models.TextField()
    Description = models.TextField()