TASK = dict(
    id='facturar-danos-despues',
    title='Facturar un daño días después de la devolución',
    short='Facturar daños después',
    cat='devolucion',
    summary='Si en la devolución marcaste daños pero **aún no sabías cuánto costaban** (el taller tenía que dar presupuesto), los facturas después desde la **ficha de la devolución**.',
    when='El taller ya te ha dado el importe de un daño de una furgoneta que ya se devolvió.',
    before=['En la devolución marcaste **El vehículo presenta daños** y dejaste el importe a 0 ([[danos-devolucion]]).',
            'Tienes el importe del presupuesto o la factura del taller.'],
    tags=['daños', 'golpe', 'rayon', 'factura daños', 'cobrar daños', 'presupuesto taller', 'despues', 'devolucion', 'desperfectos'],
    warn='Si ya devolviste **toda** la fianza al cliente, este importe lo tendrá que pagar aparte. Llámale antes para explicárselo.',
    result='La ficha de la devolución tiene el botón **Factura de Daños** con la factura al cliente.',
    next=['devolver-fianza', 'cobrar-cuotas'],
)


def run(g):
    cid = g.new_contract('2331-DMO', 'María Ejemplo López', start_in=-3, days=3, driver='María Ejemplo López')
    g.quick_return(cid, km=180, refund=False, has_damage=True, damage_amount=0, invoice_damage_now=False,
                   damage_description='<p>Golpe en el paragolpes trasero. Pendiente de presupuesto del taller.</p>')
    g.open_app()
    g.step('Pulsa **Devoluciones de Vehículos** en el menú (si no lo ves, está en el **+**).',
           marks=[g.menu('Devoluciones de Vehículos')], crop='top')
    g.go('Devoluciones de Vehículos')
    g.page.wait_for_selector('.o_list_view .o_data_row', timeout=30000)
    g.wait(800)
    row = g.page.locator('.o_data_row', has_text='2331').first
    g.step('Busca la devolución de esa furgoneta (la columna **Daños** está marcada) y ábrela.',
           marks=[row], crop='top')
    g.open_row(row)
    tab = g.tab('Inspección de Daños')
    tab.click()
    g.wait(600)
    g.fill('damage_amount', '180')
    g.step('En la pestaña **Inspección de Daños** escribe el **importe** que ha dado el taller.',
           labels=['Pestaña **Inspección de Daños**.', '**Importe de los daños**.', 'Lo que apuntaste en la devolución.'],
           marks=[tab, g.field('damage_amount'), g.field('damage_description')],
           crop=g.band(tab, g.field('damage_description')))
    g.save()
    btn = g.button(name='action_create_damage_invoice')
    g.step('Guarda. Aparece arriba el botón **Facturar Daños**: púlsalo.', marks=[btn], crop='top')
    btn.click()
    g.page.wait_for_selector('.o_form_view .o_field_widget[name=invoice_line_ids]', timeout=30000)
    g.wait(1500)
    g.step('Se crea la **factura de daños** al cliente en borrador. Revisa el importe y pulsa **Confirmar**. Después, cóbrala ([[cobrar-cuotas]]).',
           marks=[g.page.locator('.o_field_widget[name=invoice_line_ids]').first, g.button(name='action_post')],
           crop=g.page.locator('.o_form_sheet').first)
