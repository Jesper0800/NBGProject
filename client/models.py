from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'

    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    )

    ZZP = 'zzp'
    BV = 'bv'
    VOF = 'vog'
    STICHTING = 'stichting'

    CHOICES_FIRMATYPE = (
        (ZZP, 'Zzp'),
        (BV, 'Bv'),
        (VOF, 'Vof'),
        (STICHTING, 'Stichting'),
    )

    BASIC = 'basic'
    ZILVER = 'zilver'
    GOUD = 'goud'

    CHOICES_PAKKET = (
        (BASIC, 'Basic'),
        (ZILVER, 'Zilver'),
        (GOUD, 'Goud'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True,null=True)
    priority = models.CharField(max_length=10, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=NEW)
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    address_1 = models.CharField(max_length=255, default='Niet Bekend')
    address_2 = models.CharField(max_length=255, default='Niet Bekend')
    address_3 = models.CharField(max_length=255, default='Niet Bekend')
    telefoon_nummer = models.PositiveSmallIntegerField(default=0)
    woon_plaats = models.CharField(max_length=255, default='Woonplaats')
    vak_gebied = models.CharField(max_length=255, default='Vak Gebied')
    lead_datum = models.DateField(auto_now=False)
    kvk = models.PositiveSmallIntegerField(default=0)
    belasting_nummer = models.CharField(max_length=255, default='Niet Bekend')
    firma_type = models.CharField(max_length=10, choices=CHOICES_FIRMATYPE, default=ZZP)
    contact_persoon = models.CharField(max_length=255, default='Contact Persoon')
    contact_persoon_email = models.EmailField(default='EmailHierInvullen@snel.nl')
    contact_datum_1 = models.DateField(auto_now=False)
    contact_datum_2 = models.DateField(auto_now=False)
    contact_datum_3 = models.DateField(auto_now=False)
    opmerkingen = models.TextField(blank=True,null=True)
    pakket = models.CharField(max_length=10, choices=CHOICES_PAKKET, default=BASIC)
    File = models.FileField

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
class ClientFile(models.Model):
    client = models.ForeignKey('Client', related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='clientfiles')
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='client_files', on_delete=models.CASCADE)

    def __str__(self):
        return self.created_by.username
    
class Comment(models.Model):
    client = models.ForeignKey('Client', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='client_comments', on_delete=models.CASCADE)