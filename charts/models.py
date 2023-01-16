from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# User
class User(AbstractUser):
    pass
    # TEN 

# Working file
class DataFile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE) #Daniel
    workingfile = models.FileField(upload_to='data_files') # 'name.csv'
    date_created = models.DateTimeField(auto_now_add= True)
    dashboard = models.ForeignKey('Dashboard', on_delete=models.CASCADE) 

    def __str__(self):
        return self.workingfile.name



# dashboards
class Dashboard(models.Model):
    user= models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
 
    class Meta:
        unique_together= ('user', 'title')

    def __str__(self):
        return self.title

    


# charts
class Charts(models.Model):
    data = models.ForeignKey('Datafile', on_delete=models.CASCADE)
    dashboard = models.ForeignKey('dashboard', on_delete=models.CASCADE)
    X= models.CharField(max_length=60)
    Y= models.CharField(max_length=60)
    chart_type = models.CharField(
        max_length= 60,
        choices = [
            ('bar', 'bar'),
            ('pie', 'pie'),
            ('line', 'line'),
            ('doughnut', 'doughnut')
        ]
    )
  