TASK = dict(
    id='cobrar-cuotas',
    title='Facturar y cobrar el alquiler (cuotas)',
    short='Facturar y cobrar',
    cat='cobros',
    summary='El alquiler se cobra por cuotas: primero se crea el calendario de cuotas, después la factura de cada cuota, y por último se registra el pago.',
    when='Al entregar (pago completo) o cada vez que toca una cuota (alquileres largos).',
    before=['El contrato está **En curso**.',
            'La **forma de pago** está elegida en el contrato (pago completo, mensual…).'],
    tags=['factura', 'facturar', 'cobrar', 'cuota', 'pago', 'registrar pago', 'recibo', 'calendario de pagos'],
    result='La factura está **Pagada** y la cuota sale como cobrada en el contrato.',
    notes=[['info', 'En contratos por cuotas (semanal, mensual…), las facturas de cada cuota se crean **solas** el día que tocan. Tú solo tienes que registrar el cobro.'],
           ['warn', 'Sin cuotas creadas **no se puede hacer la devolución**: el botón **Devuelto** no aparece hasta que el contrato tiene su calendario de cuotas.']],
    next=['devolver'],
)


def run(g):
    g.open_contract(g.find('vehicle.contract', [['vehicle_id.license_plate', '=', '0777-DMO']])['id'])
    g.step('En el contrato **En curso**, pulsa **Crear cuota**.', marks=[g.button(name='action_create_vehicle_payment')], crop='top',
           detail='Crea el calendario de pagos según la **forma de pago** del contrato: una sola cuota si es pago completo, o una por semana / mes…')
    g.button(name='action_create_vehicle_payment').click()
    g.wait(1500)
    tab = g.tab('Detalles de pago')
    tab.click()
    g.wait(800)
    rows = g.page.locator('.o_field_widget[name=vehicle_payment_option_ids] .o_data_row')
    g.step('Abajo, en la pestaña **Detalles de pago del vehículo**, salen las cuotas con su fecha e importe.',
           labels=['Pestaña de cuotas.', 'Cada línea es una cuota. Pulsa **Crear factura** en la que toque cobrar.'],
           marks=[tab, rows.first],
           crop=g.band(g.page.locator('.o_notebook').first, g.page.locator('.o_field_widget[name=vehicle_payment_option_ids]')))
    rows.first.locator('button[name=action_create_payment_invoice]').click()
    g.wait(2000)
    g.step('Se abre la **factura en borrador**. Revisa las líneas y pulsa **Confirmar**.',
           labels=['Líneas: alquiler, seguro y fianza (la fianza va sin IVA).', 'Total a cobrar.', 'Pulsa **Confirmar**.'],
           marks=[g.page.locator('.o_field_widget[name=invoice_line_ids] .o_list_table'), g.page.locator('.o_field_widget[name=tax_totals]'),
                  g.button(name='action_post')],
           detail='Los precios de alquiler y seguro **ya llevan el IVA incluido**: la factura solo lo desglosa. El total coincide con lo que se le dijo al cliente.')
    g.button(name='action_post').click()
    g.wait(1500)
    g.step('La factura ya tiene número. Cuando el cliente pague, pulsa **Registrar pago**.',
           marks=[g.button(name='action_register_payment')], crop='top')
    g.button(name='action_register_payment').click()
    g.wait(1500)
    modal = g.page.locator('.modal-content').last
    g.step('Elige **cómo ha pagado** y comprueba el importe. Pulsa **Crear pago**.',
           labels=['**Diario**: Banco (tarjeta / transferencia) o Efectivo.', '**Importe** cobrado.', '**Fecha** del cobro.', 'Pulsa **Crear pago**.'],
           marks=[[g.label('journal_id'), g.field('journal_id')], [g.label('amount'), g.field('amount')],
                  [g.label('payment_date'), g.field('payment_date')], modal.locator('button[name=action_create_payments]')],
           crop=modal,
           tip='Si paga solo una parte, cambia el **Importe**: la factura quedará como «Pagado parcialmente» y podrás registrar el resto después.')
    modal.locator('button[name=action_create_payments]').click()
    g.wait(2000)
    g.step('Hecho: la factura sale como **Pagado** (o «En proceso de pago» hasta que el banco lo concilie).',
           marks=[g.page.locator('.ribbon, .o_widget_web_ribbon').first])
    g.page.locator('.o_breadcrumb a', has_text='VC').first.click()
    g.wait(1500)
    g.tab('Detalles de pago').click()
    g.wait(800)
    g.step('En el contrato, la cuota ya tiene su factura y su estado de pago.',
           marks=[g.page.locator('.o_field_widget[name=vehicle_payment_option_ids] .o_data_row').first],
           crop=g.band(g.page.locator('.o_notebook').first, g.page.locator('.o_field_widget[name=vehicle_payment_option_ids]')))
