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
    Description = models.TextField()    #File_Field = models.FileField(upload_to='documents/secureWitness/uploads/')  #where do I specify the location, is it here?
    File_Field = models.FileField()  #^ Can specify file path as above or use the path from settings.  Maybe pass variables here for AuthorID
    #pass variables for the username or authorID which will create the directory or path to the right directory?

    #File_Field = models.FileField(upload_to='documents/secureWitness/uploads/')  #where do I specify the location, is it here?


#to drop this table :    ctrl+alt+r, SQL clear, secure_witness_app.  will drop bulletins.
#Then remake table with syncDB

    #NOTE: To RESET the if altering structure = ctrl+alt+r, flush,?   secure_witness_app.  will drop bulletins.  careful not to drop users in AUTH or whereever
    # manage.py reset table_name
    #TODO how do you clear all Bulletins in database?  also note to sync when adding new models or fields?
