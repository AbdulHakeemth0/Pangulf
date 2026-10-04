# Copyright (C) Softhealer Technologies.

from . import models
from . import wizard


def post_init_hook(env):
    # Update old customers and vendors.
    pdc_customer = env.ref('sh_pdc.pdc_cust_account', raise_if_not_found=False)
    pdc_vendor = env.ref('sh_pdc.pdc_vendor_account', raise_if_not_found=False)

    values = {}
    if pdc_customer:
        values['pdc_customer'] = pdc_customer.id
    if pdc_vendor:
        values['pdc_vendor'] = pdc_vendor.id

    if values:
        env['res.company'].search([]).write(values)
