# Generated by Django 5.0.7 on 2024-07-13 23:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='meli_237330330',
            fields=[
                ('id_venda', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=200)),
                ('data_de_criacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('valor_pedido', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comissao_taxa_fixa', models.DecimalField(decimal_places=2, max_digits=10)),
                ('frete_cobrado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('repasse', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mlb', models.CharField(max_length=500)),
                ('titulo_anuncio', models.TextField()),
                ('sku', models.CharField(max_length=500)),
                ('quantidade', models.IntegerField()),
                ('modo_de_envio', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'meli_237330330',
                'managed': False,
            },
        ),
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
