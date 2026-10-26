TASK = dict(
    id='gasto-vehiculo',
    title='Apuntar un gasto de una furgoneta (lavado, gasoil, peaje…)',
    short='Gasto de furgoneta',
    cat='flota',
    summary='Los gastos pequeños de una furgoneta (lavado, combustible, peaje, aparcamiento…) se apuntan en su ficha, en la pestaña **Gastos del vehículo**. El gasto va solo a la **compañía dueña** de la furgoneta.',
    when='Has pagado algo para una furgoneta y tienes el ticket.',
    before=['Tienes el **ticket** o factura (foto o PDF).',
            'Sunset y Pinveco **marcadas** en el selector de compañías ([[companias]]).'],
    tags=['gasto', 'gastos', 'ticket', 'lavado', 'gasoil', 'gasolina', 'peaje', 'parking', 'aparcamiento', 'recibo', 'combustible'],
    warn='Escribe **quién** hizo el gasto en **Empleado (texto)**. Si lo dejas vacío sale el error «Indique el empleado del gasto».',
    result='El gasto queda en la ficha de la furgoneta y en la compañía dueña, listo para que contabilidad lo revise.',
    notes=['Las reparaciones de taller **no** van aquí: van en una solicitud de mantenimiento ([[mantenimiento-vehiculo]]).'],
    next=['mantenimiento-vehiculo', 'ficha-vehiculo'],
)


def run(g):
    vid = g.find('fleet.vehicle', [['license_plate', '=', '0222-DMO']])['id']
    g.url(f'/odoo/action-vehicle_rental.action_fleet_vehicle/{vid}')
    g.page.wait_for_selector('.o_form_view .o_field_widget[name=license_plate]', timeout=30000)
    g.wait(1000)
    g.check('is_any_vehicle_expense')
    g.wait(600)
    g.step('En la ficha de la furgoneta marca **¿Hay Gastos del Vehículo?**. Aparece la pestaña **Gastos del vehículo**.',
           marks=[g.field('is_any_vehicle_expense'), g.field('company_id')],
           labels=['**¿Hay Gastos del Vehículo?**', 'La **compañía** dueña: el gasto irá a ella.'],
           crop=g.page.locator('.o_form_sheet').first)
    tab = g.page.locator('.o_notebook a.nav-link[name=fleet_vehicle_expenses]').first
    tab.click()
    g.wait(600)
    lines = g.page.locator('.o_field_widget[name=fleet_expense_ids]').first
    add = lines.locator('.o_field_x2many_list_row_add a').first
    g.step('Abre la pestaña **Gastos del vehículo** y pulsa **Añadir una línea**.', marks=[tab, add], crop=g.band(tab, lines))
    add.click()
    g.page.wait_for_selector('.modal-content .o_field_widget[name=product_id]', timeout=20000)
    g.wait(1000)
    modal = g.page.locator('.modal-content').last
    g.fill('name', 'Lavado exterior')
    g.m2o('product_id', 'Gastos', pick='Gastos')
    g.fill('total_amount_currency', '15')
    g.fill('employee_name', 'Laura Mostrador')
    g.step('Rellena el gasto:',
           labels=['**Descripción**: qué es.', '**Categoría**: el tipo de gasto.', '**Total** del ticket.', '**Empleado (texto)**: quién lo pagó.'],
           marks=[g.field('name'), g.field('product_id'), g.field('total_amount_currency'), g.field('employee_name')],
           crop=modal,
           tip='Adjunta la foto del ticket con **Adjuntar recibo** (arriba en la ventana).')
    modal.locator('.modal-footer button', has_text='Guardar').first.click()
    g.wait(1200)
    g.save()
    g.step('Guarda la ficha. El gasto queda en la lista de la furgoneta.', marks=[lines], crop=g.band(tab, lines))
