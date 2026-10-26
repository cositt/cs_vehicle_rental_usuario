TASK = dict(
    id='contratos-grupo',
    title='Contrato Grupo: entregar todas y facturar en una sola factura',
    short='Contrato grupo',
    cat='cobros',
    summary='El **Contrato Grupo** junta los contratos de varias furgonetas del mismo cliente. Desde él entregas todas de una vez y haces **una sola factura** con el alquiler, la fianza y los extras de todas.',
    when='El cliente se lleva las furgonetas de una [[reserva-multiple]], o te pide una factura única por todas.',
    before=['Has creado el grupo con [[reserva-multiple]].',
            'Cada contrato del grupo está revisado (conductor, seguro, combustible): ábrelos desde la pestaña **Vehículos / Contratos**.'],
    tags=['grupo', 'contrato grupo', 'factura unica', 'factura consolidada', 'entregar todos', 'facturar periodo', 'varias furgonetas', 'empresa'],
    stop='**Entregar todos** pasa **todas** las furgonetas a **En curso** a la vez, tengan o no conductor. Púlsalo solo cuando salgan **todas**. Si sale una hoy y otra mañana, entrégalas una a una desde cada contrato ([[entregar]]).',
    result='Una sola factura en **Facturas Consolidadas** con una línea por cuota, fianza y extra de cada furgoneta.',
    notes=['**Facturar Período** solo factura lo que aún no está facturado. Si un contrato ya tenía su cuota facturada, no se repite.',
           'Si una furgoneta choca con otra reserva o le falta algo, **Entregar todos** no entrega ninguna y te dice cuál falla.'],
    next=['devolver', 'cobrar-cuotas'],
)


def run(g):
    grp = g.find('vehicle.contract.group', [['customer_id.name', '=', 'Cliente Demo SL'], ['state', '=', 'draft']])
    g.url(f"/odoo/vehicle.contract.group/{grp['id']}")
    g.page.wait_for_selector('.o_form_view .o_field_widget[name=contract_ids]', timeout=30000)
    g.wait(1000)
    contracts = g.page.locator('.o_field_widget[name=contract_ids]').first
    allbtn = g.button(name='action_activate_all')
    g.step('Abre el grupo (menú **Contratos Grupo**). Arriba están las fechas, el tipo de pago y los totales; abajo, un contrato por furgoneta.',
           labels=['**Entregar todos**.', 'Totales del grupo (alquiler y fianza).', 'Los contratos. Pulsa uno para abrirlo y revisarlo.'],
           marks=[allbtn, [g.field('total_amount'), g.field('total_deposit')], contracts],
           crop=g.page.locator('.o_form_view').first)
    allbtn.click()
    g.wait(2500)
    modal = g.page.locator('.modal-content:visible').last
    if modal.count():
        send = modal.locator('button', has_text='Enviar').first
        g.step('Sale el **correo de entrega** para el cliente. Pulsa **Enviar**.',
               marks=[send], crop=modal,
               detail='Verás el texto con **códigos** (`object.vehicle_id...`). Es normal cuando son varias furgonetas: al enviarse, cada contrato manda su propio correo con sus datos. **No borres los códigos.**')
        send.click()
        g.wait(2000)
        g.url(f"/odoo/vehicle.contract.group/{grp['id']}")
        g.page.wait_for_selector('.o_form_view .o_field_widget[name=contract_ids]', timeout=30000)
        g.wait(1000)
    contracts = g.page.locator('.o_field_widget[name=contract_ids]').first
    inv = g.button(name='action_create_consolidated_invoice')
    g.step('Todas las furgonetas están **En curso**. Para cobrar, pulsa **Facturar Período**.',
           labels=['Estado de cada contrato: **En curso**.', '**Facturar Período**.'],
           marks=[contracts.locator('td[name=status]'), inv],
           crop=g.page.locator('.o_form_view').first)
    inv.click()
    g.wait(2500)
    g.step('Se crea **una factura en borrador** con todas las líneas. Revisa los importes y pulsa **Confirmar**; luego cóbrala como siempre ([[cobrar-cuotas]]).',
           marks=[g.page.locator('.o_field_widget[name=invoice_line_ids]').first, g.button(name='action_post')],
           crop=g.page.locator('.o_form_view').first,
           warn='Mira que la fianza salga **una vez por furgoneta**. Si falta alguna, no confirmes y avisa al responsable.')
