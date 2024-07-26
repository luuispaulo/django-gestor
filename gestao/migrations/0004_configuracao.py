# Generated by Django 5.0.7 on 2024-07-25 00:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0003_delete_domain_delete_tenant'),
    ]

    operations = [
        migrations.CreateModel(
            name='configuracao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(choices=[('IMPOSTO', 'Imposto'), ('EMBALAGEM', 'Embalagem'), ('PUBLICIDADE', 'Publicidade'), ('TRANSPORTE', 'Transporte'), ('CUSTOFIXO', 'Custo Fixo'), ('LUCRATIVIDADE', 'Lucratividade')], max_length=200)),
                ('valor', models.TextField()),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
