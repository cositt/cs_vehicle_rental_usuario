TASK = dict(
    id='mantenimiento-vehiculo',
    title='Mandar una furgoneta al taller y registrar la reparación',
    short='Mantenimiento',
    cat='flota',
    summary='Si una furgoneta va al taller, pulsa **En mantenimiento**: así deja de salir en las reservas. Crea una **Solicitud de mantenimiento** con lo que se le ha hecho, pasa la factura del taller y, cuando vuelva, pulsa **Disponible**.',
    when='Una furgoneta tiene una avería, le toca revisión o va a la ITV.',
    before=['La furgoneta **no** está alquilada ahora (si lo está, primero [[devolver]] o [[sustituir]]).',
            'Tiene puesto su **Horario de Mantenimiento** en la ficha ([[ficha-vehiculo]]).'],
    tags=['taller', 'averia', 'mantenimiento', 'revision', 'itv', 'reparacion', 'mecanico', 'aceite', 'neumaticos', 'en mantenimiento', 'operacional', 'factura taller'],
    stop='Si no la marcas **En Mantenimiento**, la furgoneta sigue saliendo como libre y alguien la puede reservar mientras está en el taller.',
    result='La furgoneta tiene su solicitud con piezas y servicios, la factura del taller en borrador, y vuelve a estar **Disponible**.',
    notes=['Si la furgoneta está alquilada, el botón **En Mantenimiento** te dará el error «El vehículo … está alquilado ahora mismo».',
           'Si no tiene **Horario de Mantenimiento**, **Crear Solicitud de Mantenimiento** te pedirá que lo pongas primero.'],
    next=['ficha-vehiculo', 'disponibilidad'],
)


def seed(g):
    if not g.find('res.partner', [['name', '=', 'Taller Demo SL']]):
        g.rpc('res.partner', 'create', [{'name': 'Taller Demo SL', 'is_company': True, 'supplier_rank': 1}])


def open_vehicle(g, vid):
    g.url(f'/odoo/action-vehicle_rental.action_fleet_vehicle/{vid}')
    g.page.wait_for_selector('.o_form_view .o_field_widget[name=license_plate]', timeout=30000)
    g.wait(1000)


def run(g):
    seed(g)
    vid = g.find('fleet.vehicle', [['license_plate', '=', '2775-DMO']])['id']
    open_vehicle(g, vid)
    g.m2o('maintenance_schedule_id', 'Revisión cada 90', pick='Revisión cada 90 días (Sunset)')
    g.step('Abre la ficha de la furgoneta. Si no tiene **Horario de Mantenimiento**, pónselo y guarda.',
           marks=[g.field('maintenance_schedule_id')],
           crop=g.band(g.field('odometer'), g.field('maintenance_schedule_id')))
    g.save()
    btn = g.button(name='available_to_in_maintenance')
    g.step('Pulsa **En mantenimiento** (botón rojo).', marks=[btn], crop='top')
    btn.click()
    g.wait(1500)
    g.step('La cinta cambia a **En Mantenimiento** y arriba pone **En mantenimiento**. Ya no sale en las reservas ni en la web.',
           marks=[g.page.locator('.ribbon').first, g.page.locator('.o_statusbar_status').first],
           crop=g.page.locator('.o_form_sheet_bg').first)
    req = g.button(name='action_create_maintenance_request')
    g.step('Ahora pulsa **Crear Solicitud de Mantenimiento** (botón amarillo).', marks=[req], crop='top')
    req.click()
    g.page.wait_for_selector('.o_form_view .o_field_widget[name=fleet_vehicle_id]', timeout=30000)
    g.wait(1200)
    g.step('Se crea la solicitud con la furgoneta, los km y la **próxima revisión** calculada.',
           marks=[g.field('fleet_vehicle_id'), g.field('upcoming_maintenance_date')],
           crop=g.page.locator('.o_form_sheet').first)
    tab = g.tab('Piezas y Servicios')
    tab.click()
    g.wait(600)
    services = g.page.locator('.o_field_widget[name=vehicle_maintenance_service_ids]').first
    services.locator('.o_field_x2many_list_row_add a').first.click()
    g.wait(800)
    row = services.locator('.o_data_row').last
    inp = row.locator('[name=product_id] input').first
    inp.fill('Cambio de aceite')
    g.page.wait_for_selector('.o-autocomplete--dropdown-item', timeout=10000)
    g.page.locator('.o-autocomplete--dropdown-item', has_text='Cambio de aceite y filtros').first.click()
    g.wait(800)
    charge = row.locator('[name=service_charge] input').first
    charge.fill('120')
    charge.press('Tab')
    g.wait(600)
    g.page.keyboard.press('Escape')
    g.save()
    g.step('En **Piezas y Servicios Usados** apunta lo que ha hecho el taller: repuestos arriba, mano de obra y servicios abajo. Guarda.',
           labels=['Pestaña **Piezas y Servicios Usados**.', 'Una línea por servicio (aceite, frenos, ITV, neumáticos…) con su importe.'],
           marks=[tab, services],
           crop=g.band(tab, services))
    bill = g.button('Crear factura')
    g.step('Pulsa **Crear factura** (arriba) para pasar la factura del taller.', marks=[bill], crop='top')
    bill.click()
    g.page.wait_for_selector('.modal-content .o_field_widget[name=vendor_id]', timeout=20000)
    g.wait(800)
    modal = g.page.locator('.modal-content').last
    g.m2o('vendor_id', 'Taller Demo')
    g.step('Elige el **taller** (proveedor) y pulsa **Crear factura**.',
           marks=[g.field('vendor_id'), modal.locator('.modal-footer button').first], crop=modal)
    modal.locator('.modal-footer button').first.click()
    g.wait(2500)
    g.step('Se crea la **factura de proveedor** en borrador con las líneas. Comprueba el importe con el papel del taller y adjunta la factura.',
           marks=[g.page.locator('.o_field_widget[name=invoice_line_ids]').first],
           crop=g.page.locator('.o_form_sheet').first,
           detail='Contabilidad la confirmará y la pagará. Tú solo comprueba que el importe coincide.')
    open_vehicle(g, vid)
    ok = g.button(name='in_maintenance_to_available')
    g.step('Cuando la furgoneta vuelva del taller, abre su ficha y pulsa **Disponible** (botón verde).',
           marks=[ok], crop='top',
           warn='Si se te olvida, la furgoneta **no** sale en las reservas aunque esté lista.')
    ok.click()
    g.wait(1200)
