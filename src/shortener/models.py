from django.db import models
from django.conf import settings
from .utils import create_shortcode
# Create your models here.

SHORTCODE_MAX = getattr(settings, 'SHORTCODE_MAX', 15) # is same as setting.SHORTCODE_MAX, 15 IS A DEFAULT VALUE

class KirrURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(KirrURLManager, self).all(*args, **kwargs)
        qs = qs.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = KirrURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]            
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.shortcode)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i = new_codes) 


class KirrURL(models.Model):
    url = models.CharField(max_length=220, )
    shortcode = models.CharField(max_length=SHORTCODE_MAX,  unique=True, blank=True)
    update = models.DateTimeField(auto_now=True) #everytime the model is saved
    timestamp = models.DateTimeField(auto_now_add=True) #when model whas created
    active =  models.BooleanField(default=True)

    objects = KirrURLManager()
    
    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        super(KirrURL, self).save(*args, **kwargs)

    
    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)