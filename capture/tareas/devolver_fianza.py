TASK = dict(
    id='devolver-fianza',
    title='Devolver la fianza al cliente',
    short='Devolver fianza',
    cat='cobros',
    summary='Al hacer la devolución se crea una factura rectificativa con la fianza. Solo tienes que confirmarla y registrar que se la has devuelto.',
    when='Después de la devolución, cuando le devuelves el dinero de la fianza al cliente.',
    before=['El contrato está **Devuelto** y en la devolución se dejó marcado **Devolver la fianza** ([[devolver]]).'],
    tags=['fianza', 'deposito', 'devolver dinero', 'rectificativa', 'abono', 'reembolso', 'garantia', 'desbloquear'],
    result='La rectificativa de la fianza sale como **Pagado**: queda registrado que el cliente ha recibido su fianza.',
    notes=[['tip', '¿En la devolución **no** marcaste devolver la fianza? Usa el botón **Devolver fianza** del contrato: [[devolver-fianza-despues]].']],
    next=['devolver-fianza-despues'],
)


def run(g):
    cid = g.find('vehicle.contract', [['vehicle_id.license_plate', '=', '0777-DMO']])['id']
    g.open_contract(cid)
    g.step('En el contrato **Devuelto**, pulsa el botón **Facturas** de arriba.', marks=[g.page.locator('button[name=view_customer_invoice]')], crop='top')
    g.page.locator('button[name=view_customer_invoice]').click()
    g.wait(1500)
    row = g.page.locator('.o_data_row', has_text='Borrador').first
    g.step('Verás la factura del alquiler y la **rectificativa de la fianza** en **Borrador** (importe en negativo). Ábrela.',
           marks=[row])
    g.open_row(row)
    g.wait(1500)
    g.step('Comprueba el importe y pulsa **Confirmar**.', marks=[g.page.locator('.o_field_widget[name=invoice_line_ids] .o_list_table'), g.button(name='action_post')],
           labels=['Línea de la fianza a devolver.', 'Pulsa **Confirmar**.'])
    g.button(name='action_post').click()
    g.wait(1500)
    g.button(name='action_register_payment').click()
    g.wait(1500)
    modal = g.page.locator('.modal-content').last
    g.step('Pulsa **Registrar pago**, elige **cómo se la devuelves** (Banco si es a la tarjeta, Efectivo si es en mano) y pulsa **Crear pago**.',
           marks=[[g.label('journal_id'), g.field('journal_id')], [g.label('amount'), g.field('amount')], modal.locator('button[name=action_create_payments]')],
           labels=['Diario: cómo se devuelve.', 'Importe devuelto.', '**Crear pago**.'],
           crop=modal,
           warn='Si se pagó con **tarjeta**, la devolución se hace en el **datáfono o en Redsys** a esa misma tarjeta. Aquí solo lo apuntas.')
    modal.locator('button[name=action_create_payments]').click()
    g.wait(2000)
    g.step('Listo: la rectificativa de la fianza sale como **Pagado**.', marks=[g.page.locator('.ribbon, .o_widget_web_ribbon').first], crop='top')
