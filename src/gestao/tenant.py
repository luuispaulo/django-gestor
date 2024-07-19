from gestao.models import Tenant, Domain

tenant = Tenant(
    schema_name='public',
    name='Tenant 1',
    paid_until='2024-12-31',
    on_trial=True
)
tenant.save()


domain = Domain(
    domain='127.0.0.1',
    tenant=tenant
)
domain.save()
