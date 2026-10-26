from datetime import date, timedelta

TASK = dict(
    id='ampliar',
    title='Ampliar días a un alquiler en curso',
    short='Ampliar días',
    cat='durante',
    summary='Si el cliente quiere quedarse la furgoneta más días, se hace una ampliación: nueva fecha de fin, se firma un anexo y se factura aparte.',
    when='El cliente llama o viene porque necesita la furgoneta más tiempo.',
    before=['El contrato está **En curso** (o en Borrador).',
            'Has mirado que la furgoneta **está libre** esos días extra ([[disponibilidad]]).'],
    tags=['ampliar', 'ampliacion', 'alargar', 'mas dias', 'prorrogar', 'prorroga', 'extender', 'anexo', 'nueva fecha'],
    result='El contrato tiene la **nueva fecha de fin**, el anexo firmado y la **factura de la ampliación**.',
    next=['cobrar-cuotas'],
)


def run(g):
    cid = g.new_contract('0333-DMO', 'Cliente Demo SL', start_in=-1, days=3, driver='Pepe Demo García')
    g.open_contract(cid)
    g.step('En el contrato, pulsa **Ampliar contrato**.', marks=[g.button(name='action_new_extension')], crop='top')
    g.button(name='action_new_extension').click()
    g.wait(2000)
    sc = g.scope()
    g.fill('new_end_date', (date.today() + timedelta(days=6)).strftime('%d/%m/%Y 09:00:00'))
    g.step('Pon la **nueva fecha de fin**. Los días, el precio y el importe se calculan solos.',
           labels=['**Fecha de fin original** del contrato.', '**Nueva fecha de fin**.', 'Días de ampliación (días enteros, como el contrato).',
                   '**Tarifa por día** de todo el alquiler con los días nuevos, e **importe**: solo lo que falta por cobrar.'],
           marks=[g.field('original_end_date'), [g.label('new_end_date'), g.field('new_end_date')], g.field('extension_days'),
                  [g.field('daily_rate'), g.field('extension_amount')]],
           crop=sc.locator('.o_form_sheet').first if sc.locator('.o_form_sheet').count() else None,
           detail='Al alargar, el alquiler puede pasar a un tramo más barato. Ejemplo: 2 días a 97 € = 194 € ya cobrados; con un día más son 3 días del tramo 3-5 días a 85 € = 255 €, así que la ampliación cobra **61 €**.',
           warn='La nueva fecha tiene que ser **posterior** a la fecha de fin actual.')
    if g.page.locator('.modal-content').count():
        g.page.locator('.modal-content').last.locator('button.o_form_button_save, button', has_text='Guardar').first.click()
        g.wait(1500)
    else:
        g.save()
    g.step('Guarda. Ahora toca **firmar el anexo**: envíalo a firmar por correo, o márcalo como firmado si lo firma en papel.',
           labels=['**Enviar a firmar**: le llega al cliente para firmar en el móvil.', '**Marcar como firmado**: si ha firmado en papel.'],
           marks=[g.button(name='action_send_to_sign'), g.button(name='action_mark_signed')], crop='top')
    g.button(name='action_mark_signed').click()
    g.wait(1500)
    g.step('Con el anexo **Firmado**, pulsa **Crear factura** para cobrar los días extra.', marks=[g.button(name='action_create_extension_invoice')], crop='top',
           detail='La factura de la ampliación se cobra igual que las demás: Confirmar y Registrar pago ([[cobrar-cuotas]]).')
    g.button(name='action_create_extension_invoice').click()
    g.page.wait_for_selector('.o_form_view .o_field_widget[name=invoice_line_ids]', timeout=30000)
    g.wait(1500)
    g.step('Se abre la factura de la ampliación en borrador: **Confirmar** y después **Registrar pago**, como siempre.',
           marks=[g.page.locator('.o_field_widget[name=invoice_line_ids] .o_list_table'), g.button(name='action_post')])
