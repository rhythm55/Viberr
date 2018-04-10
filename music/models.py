from django.db import models
from django.core.urlresolvers import reverse

class Album(models.Model):
    user=models.foreignKey(User,default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genere = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite=models.booleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title+' - '+self.artist


class song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    is_favorite=models.BooleanField(default=False)

    def __str__(self):
     return self.song_title