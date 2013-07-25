from django.db import models

# DB model for feedreader


class Feed(models.Model):
    #id = models.BigIntegerField(db_index=True, blank=False)
    userId = models.IntegerField(blank=False)
    name = models.CharField(max_length=20, blank=False)
    url = models.CharField(max_length=500, blank=False)

    def __str__(self):
        return "userId=" + str(self.userId) + ", name='" + self.name + "', url='" + self.url + "'"