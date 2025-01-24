import datetime
from django.db import migrations, models
from pytz import utc

class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0010_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 1, 27, 5, 55, 47, 607789, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
