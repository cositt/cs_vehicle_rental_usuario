TASK = dict(
    id='cargos-extra',
    title='Cobrar un extra: fuera de horario, otra delegación, combustible, baliza',
    short='Cargos extra',
    cat='cobros',
    summary='Los **recargos** (entrega fuera de horario, devolver en otra delegación, depósito no lleno, pérdida de baliza…) se apuntan en la pestaña **Servicios extra** del contrato y se facturan con un botón.',
    when='El cliente pide algo que tiene recargo, o lo descubres al devolver.',
    before=['El contrato está en **Borrador** o **En curso** (en uno devuelto o cancelado ya no se puede).'],
    tags=['extra', 'recargo', 'suplemento', 'fuera de horario', 'otra delegacion', 'combustible', 'gasolina', 'gasoil', 'baliza', 'servicios extra', 'cargo adicional'],
    warn='Factura los extras **antes** de cerrar el contrato: cuando está devuelto la pestaña ya no se puede tocar.',
    result='El contrato tiene una **factura de servicio adicional** con los extras. Cóbrala como cualquier otra ([[cobrar-cuotas]]).',
    notes=['El importe de cada recargo sale solo, pero lo puedes cambiar en la línea.',
           'Si el combustible no está lleno, añade el recargo **y** otra línea con el importe del combustible.'],
    next=['cobrar-cuotas', 'devolver'],
)


def run(g):
    cid = g.new_contract('1665-DMO', 'Cliente Demo SL', start_in=-1, days=4, driver='Pepe Demo García')
    g.open_contract(cid)
    tab = g.page.locator('.o_notebook a.nav-link[name=extra_service]').first
    tab.click()
    g.wait(600)
    lines = g.page.locator('.o_field_widget[name=extra_service_ids]').first
    add = lines.locator('.o_field_x2many_list_row_add a').first
    g.step('En el contrato, abre la pestaña **Servicios extra** y pulsa **Añadir una línea**.', marks=[tab, add], crop=g.band(tab, lines))
    add.click()
    g.wait(800)
    row = lines.locator('.o_data_row').last
    inp = row.locator('[name=product_id] input').first
    inp.fill('Recargo: entrada')
    g.page.wait_for_selector('.o-autocomplete--dropdown-item', timeout=10000)
    g.page.locator('.o-autocomplete--dropdown-item', has_text='fuera de horario').first.click()
    g.wait(900)
    g.page.keyboard.press('Escape')
    g.wait(400)
    g.save()
    g.step('Elige el **recargo**. El importe sale solo. Guarda.',
           labels=['El recargo (escribe «Recargo» y salen todos).', 'Importe y total.'],
           marks=[lines.locator('td[name=product_id]').last, [lines.locator('td[name=amount]').last, lines.locator('td[name=total_service_charge]').last]],
           crop=g.band(tab, lines))
    btn = g.button(name='action_create_extra_service_charge_invoice')
    g.step('Pulsa **Crear factura de servicio adicional** (arriba).', marks=[btn], crop='top')
    btn.click()
    g.wait(2500)
    if g.page.locator('.o_form_view .o_field_widget[name=invoice_line_ids]').count():
        g.step('Se crea la factura en borrador con los extras. Revísala y pulsa **Confirmar**; después cóbrala.',
               marks=[g.page.locator('.o_field_widget[name=invoice_line_ids]').first, g.button(name='action_post')],
               crop=g.page.locator('.o_form_sheet').first)
    else:
        g.step('La factura queda enlazada en el contrato, en **Factura de servicio adicional**. Ábrela, confírmala y cóbrala.',
               marks=[g.field('extra_service_invoice_id')], crop=g.band(g.field('extra_service_invoice_id'), g.field('extra_service_invoice_id')))
