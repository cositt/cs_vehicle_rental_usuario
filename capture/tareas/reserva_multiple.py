from datetime import date, timedelta

TASK = dict(
    id='reserva-multiple',
    title='Reservar varias furgonetas para un mismo cliente',
    short='Reserva múltiple',
    cat='reservas',
    summary='Cuando una empresa se lleva **dos o más furgonetas** a la vez, en vez de hacer los contratos de uno en uno haces una **Reserva Múltiple**: añades las furgonetas y al final se crean de golpe un **Contrato Grupo** y un contrato por cada furgoneta.',
    when='Un cliente pide varias furgonetas para las mismas fechas (o parecidas).',
    before=['El cliente ya está dado de alta ([[nuevo-cliente]]).',
            'Sabes qué tipos de furgoneta quiere, fechas y kilómetros.'],
    tags=['varias furgonetas', 'varios vehiculos', 'flota', 'empresa', 'grupo', 'multiple', 'reserva multiple', 'lote'],
    warn='Mientras la reserva está en **Borrador** no se ha creado ningún contrato: las furgonetas **no** quedan bloqueadas para otros. No la dejes a medias.',
    result='Tienes un **Contrato Grupo** con un contrato en **Borrador** por cada furgoneta. Sigue en [[contratos-grupo]].',
    next=['contratos-grupo'],
)


def d(days, hour='08:00:00'):
    return (date.today() + timedelta(days=days)).strftime('%d/%m/%Y ') + hour


def add_vehicle(g, plate, category=None, first=False):
    g.button(name='action_add_vehicle').click()
    g.page.wait_for_selector('.modal-content .o_field_widget[name=selected_category_id]', timeout=20000)
    g.wait(1000)
    modal = g.page.locator('.modal-content').last
    if first:
        g.fill('start_date', d(0))
        g.fill('end_date', d(3))
        g.m2o('selected_category_id', category)
        g.select('km_range', '350 Km')
    elif category:
        g.m2o('selected_category_id', category)
    g.wait(1200)
    return modal, modal.locator('.o_data_row', has_text=plate)


def run(g):
    g.open_app()
    g.step('Pulsa **Reserva Múltiple** en el menú.', marks=[g.menu('Reserva Múltiple')], crop='top')
    g.go('Reserva Múltiple')
    new = g.page.locator('.o_control_panel button', has_text='Nuevo').first
    new.click()
    g.wait(1500)
    g.m2o('customer_id', 'Cliente Demo SL')
    g.step('Pulsa **Nuevo** y elige el **Cliente**. Revisa el tipo de pago y la tarjeta de la fianza.',
           labels=['**Cliente**.', '**Tipo de Pago** y **Tipo de Tarjeta**: valen para todas las furgonetas.', '**Añadir Vehículo**.'],
           marks=[g.field('customer_id'), [g.field('payment_type'), g.field('deposit_card_type')], g.button(name='action_add_vehicle')],
           crop=g.page.locator('.o_form_view').first)
    modal, row = add_vehicle(g, '0111', 'Tipo A', first=True)
    g.step('Se abre la misma ventana que en [[reservar|Reservar Vehículo]]: fechas, tipo y km. Pulsa **Reservar** en la furgoneta.',
           labels=['Fechas de recogida y devolución.', 'Tipo, km y precio.', '**Reservar** en la que quieras.'],
           marks=[[g.field('start_date'), g.field('end_date')],
                  [g.field('selected_category_id'), g.field('km_range'), g.field('calculated_price')],
                  row.locator('button', has_text='Reservar')],
           crop=modal,
           detail='Aquí **Reservar** no crea el contrato: solo añade la furgoneta a la lista de la reserva múltiple.')
    row.locator('button', has_text='Reservar').click()
    g.wait(1800)
    modal, row = add_vehicle(g, '2553', 'Tipo Z')
    g.step('Pulsa otra vez **Añadir Vehículo**. Las fechas y los km **ya vienen puestos** de la anterior: cambia solo el tipo si hace falta y pulsa **Reservar**.',
           marks=[[g.field('start_date'), g.field('end_date')], g.field('selected_category_id'), row.locator('button', has_text='Reservar')],
           crop=modal,
           tip='La furgoneta que ya has añadido **no** vuelve a salir en la lista: no puedes meterla dos veces.')
    row.locator('button', has_text='Reservar').click()
    g.wait(1800)
    lines = g.page.locator('.o_field_widget[name=line_ids]').first
    create = g.button(name='action_create_group')
    g.step('Revisa la lista: una fila por furgoneta con sus fechas y su precio por día. Cuando esté todo, pulsa **Crear Reserva Múltiple**.',
           labels=['Las furgonetas de la reserva.', '**Crear Reserva Múltiple**.'],
           marks=[lines, create], crop=g.page.locator('.o_form_view').first,
           detail='¿Te has equivocado de furgoneta? Borra la fila con la papelera antes de crear.')
    create.click()
    g.wait(1200)
    dialog = g.page.locator('.modal-content').last
    ok = dialog.locator('.modal-footer button').first
    g.step('Te pide confirmación. Pulsa **Aceptar**.', marks=[ok], crop=dialog)
    ok.click()
    g.page.wait_for_selector('.o_form_view .o_field_widget[name=contract_ids]', timeout=30000)
    g.wait(1500)
    g.step('Listo: se ha creado el **Contrato Grupo** con un contrato por furgoneta, todos en **Borrador**.',
           labels=['Nombre del grupo.', 'Un contrato por furgoneta.'],
           marks=[g.field('name'), g.page.locator('.o_field_widget[name=contract_ids]').first],
           crop=g.page.locator('.o_form_view').first)
