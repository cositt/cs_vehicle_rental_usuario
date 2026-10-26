import json
from datetime import date, datetime, time, timedelta

TASK = dict(
    id='consulta-web',
    title='Reserva hecha en la web: convertirla en contrato',
    short='Reserva web',
    cat='web',
    summary='Cuando un cliente reserva y **paga en la web**, en Odoo aparece una **Consulta de Reserva** con sus datos, fechas y tipo de furgoneta, pero **sin furgoneta concreta**. Tú eliges la furgoneta y creas el contrato con un botón.',
    when='Te llega el aviso de una reserva web, o ves una tarjeta nueva en **Consultas de Reserva**.',
    before=['El cliente ya ha pagado en la web (alquiler + fianza).'],
    tags=['web', 'internet', 'online', 'reserva web', 'consulta', 'oportunidad', 'crm', 'lead', 'redsys', 'pago online', 'pagina web'],
    stop='Antes de crear el contrato comprueba que hay furgoneta de ese tipo **libre** esas fechas ([[disponibilidad]]). El cliente ya ha pagado: si no hay furgoneta, avisa al responsable **ya**.',
    result='El contrato queda en **Borrador** con el precio pagado en la web y una línea **Pago online Redsys** en sus pagos. La consulta pasa a **Ganado** y desaparece de la lista.',
    notes=['El cliente, el DNI, el carnet y la dirección se copian solos de la web al contrato. Revísalos igualmente ([[revisar-contrato]]).',
           'Una consulta por teléfono también se puede pasar a contrato con este botón, pero entonces el precio sale a **0** y tienes que ponerlo tú.'],
    next=['revisar-contrato', 'documentos-cliente', 'entregar'],
)

FMT = '%Y-%m-%d %H:%M:%S'


def seed(g):
    """A paid web booking like the one Redsys leaves (demo data only)."""
    cat = g.find('fleet.vehicle.model.category', [['name', 'ilike', 'Tipo C']])['id']
    price, _dur = g.tariff(cat, 3, '350')
    start = datetime.combine(date.today() + timedelta(days=2), time(8, 0))
    end = start + timedelta(days=3)
    partner = g.rpc('res.partner', 'create', [{
        'name': 'Ana Web Ruiz', 'email': 'ana.web@ejemplo.es', 'phone': '600 000 006',
        'street': 'C/ Ficticia, 3', 'city': 'Málaga', 'zip': '29002'}])
    booking = {'customer_name': 'Ana Web Ruiz', 'customer_email': 'ana.web@ejemplo.es',
               'selected_price': price, 'total_price': price * 3, 'num_days': 3,
               'deposit_amount': 300.0, 'location': 'Málaga', 'category_id': cat,
               'start_time': '08:00', 'end_time': '08:00'}
    tx = g.rpc('payment.transaction', 'create', [{
        'provider_id': 18, 'payment_method_id': 39, 'amount': price * 3, 'currency_id': 126,
        'partner_id': partner, 'reference': 'WEB-DEMO-0001', 'state': 'done',
        'booking_data_json': json.dumps(booking)}])
    g.rpc('crm.lead', 'create', [{
        'name': 'Consulta de Reserva - Ana Web Ruiz', 'partner_id': partner, 'company_id': 1,
        'type': 'opportunity', 'email_from': 'ana.web@ejemplo.es', 'phone': '600 000 006', 'stage_id': 1,
        'start_date': start.strftime(FMT), 'end_date': end.strftime(FMT), 'selected_category_id': cat,
        'customer_dni': '44444444A', 'customer_address': 'C/ Ficticia, 3, 29002 Málaga',
        'driver_license_number': '44444444A', 'driver_license_issue_date': '2015-05-10',
        'driver_license_expiry_date': '2035-05-10', 'birth_date': '1990-07-21',
        'location': 'Málaga', 'start_time': '08:00', 'end_time': '08:00', 'selected_price': price,
        'payment_transaction_id': tx,
        'description': 'Reserva procesada vía web (ejemplo)<br/>Tarifa: %.2f €/día · Fianza: 300,00 €' % price}])


def run(g):
    seed(g)
    g.open_app()
    g.step('Pulsa **Consultas de Reserva** en el menú.', marks=[g.menu('Consultas de Reserva')], crop='top')
    g.go('Consultas de Reserva')
    card = g.page.locator('.o_kanban_record', has_text='Ana Web Ruiz').first
    card.wait_for(timeout=20000)
    g.step('Cada tarjeta es una reserva **pagada** en la web. Ábrela.', marks=[card], crop='top')
    card.click()
    g.page.wait_for_selector('.o_form_view', timeout=30000)
    g.wait(1000)
    tab = g.tab('Detalles de Consulta de Reserva')
    tab.click()
    g.wait(600)
    g.step('En la pestaña **Detalles de Consulta de Reserva** tienes lo que pidió el cliente.',
           labels=['Pestaña **Detalles de Consulta de Reserva**.', 'Fechas de recogida y devolución.', 'DNI y carnet que escribió en la web.'],
           marks=[tab, [g.field('start_date'), g.field('end_date')],
                  [g.field('customer_dni'), g.field('driver_license_number')]],
           crop=g.band(tab, g.field('birth_date')),
           tip='En **Notas internas** (primera pestaña) sale el resumen del pago: tarifa, fianza y total pagado.')
    create = g.page.locator('.o_form_statusbar button', has_text='Crear Contrato').first
    g.step('Pulsa **Crear Contrato** (arriba).', marks=[create], crop='top')
    create.click()
    g.page.wait_for_selector('.modal-content .o_field_widget[name=vehicle_id]', timeout=20000)
    g.wait(1200)
    modal = g.page.locator('.modal-content').last
    g.m2o('vehicle_id', '0555')
    g.step('Elige la **furgoneta** concreta y revisa fechas y kilómetros. Pulsa **Crear Contrato**.',
           labels=['**Vehículo Disponible**: solo salen las del tipo reservado.', 'Fechas de recogida y devolución (vienen de la web).',
                   '**Rango de Km**.', '**Crear Contrato**.'],
           marks=[g.field('vehicle_id'), [g.field('start_date'), g.field('end_date')], g.field('km_range'),
                  modal.locator('.modal-footer button', has_text='Crear Contrato')],
           crop=modal,
           detail='Mejor una furgoneta de la delegación donde recoge el cliente (la ves en [[disponibilidad]]).')
    modal.locator('.modal-footer button', has_text='Crear Contrato').first.click()
    g.page.wait_for_selector('.o_form_view .o_statusbar_status', timeout=30000)
    g.wait(2000)
    g.step('Ya tienes el contrato en **Borrador** con los datos de la web. Sigue con [[revisar-contrato]].',
           labels=['Estado **Borrador**.', 'Cliente y DNI copiados de la web.'],
           marks=[g.page.locator('.o_statusbar_status'), [g.field('customer_id'), g.field('customer_dni')]],
           crop='top')
