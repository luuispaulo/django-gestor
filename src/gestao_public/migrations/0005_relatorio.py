# Generated by Django 5.0.7 on 2024-07-17 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_public', '0004_delete_relatorio'),
    ]

    operations = [
        migrations.CreateModel(
            name='relatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('setor', models.CharField(choices=[('COMPRAS', 'Compras'), ('FINANCEIRO', 'Financeiro'), ('LOGISTICA', 'Logística'), ('COMERCIAL', 'Comercial'), ('RH', 'RH'), ('DIRETORIA', 'Diretoria')], max_length=20)),
                ('src', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
