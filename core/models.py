from django.db import models


class Profession(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class DataSheet(models.Model):
    description = models.CharField(max_length=250)
    historical_data = models.TextField()

    def __str__(self):
        return self.description


class Customer(models.Model):
    name = models.CharField(max_length=50)
    addr = models.TextField()
    profession = models.ManyToManyField(Profession)
    data_sheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    @property
    def profession_titles(self):
        pids = [p.id for p in self.profession.all()]
        profs = Profession.objects.filter(id__in=pids)
        return [p.description for p in profs]
    
    def num_profs(self):
        return self.profession.all().count()

    def __str__(self):
        return self.name


class Document(models.Model):
    ID = 'ID'
    PP = 'PP'
    OT = 'OT'

    DOC_TYPES = (
        (ID, 'Identity Card'),
        (PP, 'Passport'),
        (OT, 'Others'),
    )

    dtype = models.CharField(choices=DOC_TYPES, max_length=2)
    doc_num = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_num
