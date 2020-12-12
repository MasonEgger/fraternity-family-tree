from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Chapter(models.Model):
    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
    name = models.CharField(max_length=32, unique=True)
    university = models.CharField(max_length=256)
    founders_day = models.DateField()
    street_address = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

class PledgeClass(models.Model):
    class Meta:
        verbose_name = "Pledge Class"
        verbose_name_plural = "Pledge Classes"
        ordering = ['date_initiated']
    name = models.CharField(max_length=32, unique=True)
    date_initiated = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name + " - " + str(self.date_initiated)

    def get_name(self):
        return self.name

class Brother(MPTTModel):
    class Meta:
        verbose_name = "Brother"
        verbose_name_plural = "Brothers"
        ordering = ['pledge_class', 'last_name', 'first_name']

    MEMBERSHIP_STATUSES = (
        ("Alumnus", "Alumnus"),
        ("Expelled - Automatic", "Expelled - Automatic"),
        ("Expelled - Chapter", "Expelled - Chapter"),
        ("Expelled - National/COS", "Expelled - National/COS"),
        ("Honarary", "Honarary"),
        ("Good Standing", "Good Standing"),
        ("Suspended - Automatic", "Suspended - Automatic"),
        ("Suspended - Chapter", "Suspended - Chapter"),
        ("Suspended - Unknown", "Suspended - Unknown"),
        ("Probationary", "Probationary"),
    )
    membership_id = models.IntegerField()
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    address = models.CharField(max_length=512, blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pledge_class = models.ForeignKey(PledgeClass, on_delete=models.DO_NOTHING)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='littles', db_index=True, on_delete=models.DO_NOTHING)
    membership_status = models.CharField(max_length=32, choices=MEMBERSHIP_STATUSES, default="Alumnus")
    deceased = models.BooleanField(default=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.DO_NOTHING)
    bio = models.TextField(blank=True, null=True)


    class MPTTMeta:
        order_insertion_by = ['pledge_class', 'last_name']

    def __str__(self):
        return self.last_name + ", " + self.first_name

    def list_name_display(self):
        return self.__str__() + " @ " + self.pledge_class.name
