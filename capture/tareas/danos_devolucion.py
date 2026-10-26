TASK = dict(
    id='danos-devolucion',
    title='La furgoneta vuelve con daños',
    short='Daños en la devolución',
    cat='devolucion',
    summary='Si al recogerla hay un golpe o rayón nuevo: lo marcas en el dibujo de la furgoneta, pones el importe y se descuenta de la fianza.',
    when='En la devolución encuentras un daño que no estaba al salir.',
    before=['Has comprobado con el cliente que el daño **es nuevo** (míralo en el informe de salida o en las fotos del contrato).',
            'Sabes el importe, o al menos una estimación. Si no, puedes dejarlo a 0 y facturarlo después.'],
    tags=['golpe', 'rayon', 'abolladura', 'desperfecto', 'danos', 'dibujo', 'marcar danos', 'factura de danos', 'descontar fianza'],
    result='El contrato queda **Devuelto**, el daño queda dibujado en el acta y se crea la **factura de daños**. La fianza se devuelve menos los daños.',
    next=['devolver-fianza', 'facturar-danos-despues'],
)


def run(g):
    cid = g.new_contract('0555-DMO', 'María Ejemplo López', start_in=-2, days=2, driver='María Ejemplo López')
    g.open_contract(cid)
    g.button(name='b_in_progress_to_c_return').click()
    g.wait(2000)
    modal = g.page.locator('.modal-content').last
    g.fill('odometer', str(int(g.find('fleet.vehicle', [['license_plate', '=', '0555-DMO']], ('odometer',))['odometer']) + 240))
    g.select('fuel_level', 'Lleno')
    g.check('inspection_done')
    g.check('has_damage')
    g.step('Haz la devolución como siempre ([[devolver]]): km, combustible e inspección. Después marca **El vehículo presenta daños** y pulsa **Marcar daños sobre imagen**.',
           marks=[[g.label('has_damage'), g.field('has_damage')], g.button(name='action_open_damage_painter')],
           crop=g.band(g.sep('Inspección'), g.field('damage_amount')))
    g.button(name='action_open_damage_painter').click()
    g.wait(2500)
    pm = g.page.locator('.modal-content').last
    canvas = pm.locator('canvas').first
    pm.locator('.damage_tool[data-tool=circle]').click()
    g.draw(canvas, [[(.25, .42), (.31, .50)]])
    pm.locator('.damage_tool[data-tool=arrow]').click()
    g.draw(canvas, [[(.10, .25), (.24, .40)]])
    g.step('Se abre el **dibujo de la furgoneta** (frontal, laterales, techo y trasera). Marca dónde está el daño:',
           labels=['Elige la herramienta: **Círculo** para rodear el golpe, **Flecha** para señalarlo, **Texto** para escribir.',
                   'Dibuja sobre la furgoneta, en la vista que toque.',
                   'Pulsa **Guardar** y después **Volver a la Devolución**.'],
           marks=[pm.locator('.damage_tool'), canvas, [pm.locator('.damage_save, .btn-success', has_text='Guardar').first,
                                                         pm.locator('button', has_text='Volver a la Devolución')]],
           crop=pm, tip='¿Te has equivocado? **Deshacer** quita la última marca y **Limpiar** las borra todas.')
    pm.locator('.btn-success', has_text='Guardar').first.click()
    g.wait(1500)
    pm.locator('button', has_text='Volver a la Devolución').click()
    g.wait(2500)
    modal = g.page.locator('.modal-content').last
    g.fill('damage_description', 'Rayón y bollo en puerta lateral izquierda')
    g.fill('damage_amount', '250')
    g.check('invoice_damage_now')
    g.step('De vuelta en la devolución ya ves el dibujo. Completa los datos del daño:',
           labels=['Dibujo con las marcas (puedes **Editar marcas** o **Quitar marcas**).',
                   '**Descripción**: qué es y dónde. Sale en el acta.',
                   '**Importe estimado de daños**.',
                   '**Facturar los daños ahora**: crea la factura de daños al confirmar.'],
           marks=[g.field('painted_damage_image'), g.field('damage_description'), [g.label('damage_amount'), g.field('damage_amount')],
                  [g.label('invoice_damage_now'), g.field('invoice_damage_now')]],
           crop=g.band(g.sep('Inspección'), g.field('invoice_damage_now')),
           tip='¿Aún no sabes cuánto cuesta? Deja el importe a **0**: podrás facturarlo más adelante desde la ficha de la devolución ([[facturar-danos-despues]]).')
    g.step('En **Fianza** no toques nada: se devuelve la fianza entera y el sistema **resta los daños** en el **Neto a devolver**.',
           marks=[g.field('deposit_charged'), g.field('deposit_to_refund'), g.field('deposit_net_to_customer')],
           labels=['Fianza cobrada: 300 €.', '**Fianza a devolver**: la fianza entera (300 €).', '**Neto a devolver**: 300 − 250 de daños = **50 €** al cliente.'],
           crop=g.band(g.sep('Fianza'), g.field('deposit_to_refund')),
           detail='Se crean dos documentos: la **devolución de la fianza** (300 €) y la **factura de daños** (250 €). Al pagar, se compensan y el cliente recibe la diferencia.',
           warn='Si los daños **superan la fianza**, el neto sale en negativo: es lo que **el cliente tiene que pagar** de más.')
    g.check('request_signature')
    g.sign('customer_signature')
    g.sign('company_signature')
    modal = g.page.locator('.modal-content').last
    modal.locator('button[name=action_confirm_return]').click()
    g.wait(2500)
    g.step('Firma como en una devolución normal y pulsa **Confirmar Devolución**. El contrato queda **Devuelto** y ahora tiene la **factura de daños**.',
           marks=[g.page.locator('.o_statusbar_status'), g.page.locator('button[name=view_customer_invoice]')], crop='top')
    g.page.locator('button[name=action_view_returns]').click()
    g.wait(1500)
    if g.page.locator('.o_list_view').count():
        g.open_row(g.page.locator('.o_data_row').first)
        g.wait(1500)
    g.step('En la ficha de la **Devolución** (botón **Devoluciones**) tienes todo: km, daños, dibujo, y los botones del acta y la factura.',
           labels=['**Generar Acta**: el PDF de la devolución con el dibujo.', '**Factura de Daños**: abre la factura.'],
           marks=[g.button(name='action_generate_acta'), g.button(name='action_view_damage_invoice')])
