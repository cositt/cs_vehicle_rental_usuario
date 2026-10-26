TASK = dict(
    id='cancelar',
    title='Cancelar un contrato (y cobrar el cargo de cancelación)',
    short='Cancelar',
    cat='cancelar',
    summary='Si el cliente anula la reserva, cancelas el contrato. La furgoneta queda libre. Si según la política hay que cobrar algo, se hace la factura del cargo.',
    when='El cliente llama para anular, o no se presenta.',
    before=['El contrato está en **Borrador** o **En curso** (un contrato Devuelto no se cancela).',
            'Sabes si hay que cobrar cargo según la **política de cancelación** (cuántos días antes avisa).'],
    tags=['cancelar', 'anular', 'anulacion', 'cancelacion', 'no se presenta', 'cargo de cancelacion', 'penalizacion'],
    result='El contrato queda **Cancelado**, la furgoneta libre y, si había cargo, su **factura** lista para confirmar y cobrar.',
    notes=[['info', '¿Ya había pagado y la cancelación es **sin cargo**? No hagas la factura del cargo: devuelve lo cobrado con una rectificativa de su factura. ¿Tenía fianza? [[devolver-fianza-despues]].']],
    next=['devolver-fianza-despues'],
)


def run(g):
    cid = g.new_contract('2109-DMO', 'Cliente Demo SL', start_in=1, days=4, deliver=False)
    g.open_contract(cid)
    g.step('Abre el contrato y pulsa **Cancelar** (el botón rojo de arriba).', marks=[g.button(name='c_return_to_d_cancel')], crop='top',
           stop='No confundas este **Cancelar** (anula el contrato) con el **Cancelar** de las ventanas, que solo cierra la ventana.')
    g.button(name='c_return_to_d_cancel').click()
    g.wait(1500)
    dlg = g.page.locator('.modal-content').last
    g.step('Te pide confirmación. Pulsa **Aceptar**.', marks=[dlg.locator('.modal-footer button').first], crop=dlg)
    dlg.locator('.modal-footer button').first.click()
    g.wait(2000)
    tab = g.tab('cancelación')
    tab.click()
    g.wait(800)
    g.m2o('cancellation_policy_id', 'menos de 48')
    g.fill('cancellation_charge', '50')
    g.fill('cancellation_reason', 'El cliente anula el día antes de la recogida.')
    g.step('El contrato ya está **Cancelado**. Si hay que cobrar, ve a la pestaña **Política de cancelación**:',
           labels=['Pestaña de la cancelación.', '**Política**: elige la que corresponde (según con cuánto tiempo avisa).', '**Cargo de cancelación**: el importe a cobrar.', '**Motivo**: por qué se cancela.'],
           marks=[tab, g.field('cancellation_policy_id'), g.field('cancellation_charge'), g.field('cancellation_reason')],
           crop=g.band(tab, g.field('cancellation_reason')))
    g.save()
    g.step('Guarda y pulsa **Cargo de cancelación**.', marks=[g.button(name='cancellation_charge_invoice')], crop='top',
           warn='Si dejas el cargo a **0** te dará el error «Indique el importe del cargo de cancelación». Si es **sin cargo**, simplemente no pulses este botón.')
    g.button(name='cancellation_charge_invoice').click()
    g.wait(2500)
    g.step('Se crea la **factura del cargo** en borrador. Confírmala y regístrala como cualquier factura ([[cobrar-cuotas]]).',
           marks=[g.page.locator('.o_field_widget[name=invoice_line_ids] .o_list_table'), g.button(name='action_post')])
