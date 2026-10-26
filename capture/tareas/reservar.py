from datetime import date, timedelta

TASK = dict(
    id='reservar',
    title='Reservar una furgoneta (asistente)',
    cat='reservas',
    summary='La forma rápida de hacer un contrato: eliges cliente, fechas y tipo, y el sistema te enseña qué furgonetas están libres esas fechas.',
    when='Un cliente pide una furgoneta en el mostrador o por teléfono.',
    before=['El cliente ya existe en **Clientes** (si no, créalo primero).',
            'Sabes las fechas y horas de recogida y devolución.',
            'Tienes marcadas **las dos compañías** (Sunset y Pinveco) arriba a la derecha.'],
    tags=['alquilar', 'reserva', 'contrato nuevo', 'furgo', 'coche', 'nuevo alquiler', 'reservar vehiculo'],
    result='Se abre el contrato nuevo en estado **Borrador**. Todavía no se ha entregado nada: revisa los datos y sigue con «Entregar la furgoneta».',
    next=['entregar'],
)


def d(days, hour='09:00:00'):
    return (date.today() + timedelta(days=days)).strftime('%d/%m/%Y ') + hour


def run(g):
    g.open_app()
    g.step('Pulsa **Reservar Vehículo** en el menú de arriba.', marks=[g.menu('Reservar Vehículo')], crop='top')
    g.go('Reservar Vehículo')
    modal = lambda: g.page.locator('.modal-content').last
    g.m2o('customer_id', 'Cliente Demo')
    g.fill('start_date', d(0, '08:00:00'))
    g.fill('end_date', d(3, '08:00:00'))
    g.step('Rellena **quién** y **cuándo**:',
           labels=['**Cliente**: escribe unas letras del nombre y elígelo de la lista.',
                   '**Fecha de inicio**: día y hora en que se lleva la furgoneta.',
                   '**Fecha final**: día y hora en que la devuelve. El **Nº de días** se calcula solo (también puedes escribir los días y se calcula la fecha final).'],
           marks=[[g.label('customer_id'), g.field('customer_id')],
                  [g.label('start_date'), g.field('start_date')],
                  [g.label('end_date'), g.field('end_date'), g.field('rental_days')]],
           crop=modal(),
           tip='No toques **Compañía**: el contrato se pasa solo a la compañía dueña de la furgoneta que elijas.')
    g.m2o('selected_category_id', 'Tipo D')
    g.select('km_range', '350 Km')
    g.step('Elige **qué** necesita y con cuántos kilómetros:',
           labels=['**Tipo de Vehículo**: la categoría (Tipo D = furgoneta 8 m³, etc.).',
                   '**Duración**: se pone sola según los días.',
                   '**Rango de Km**: kilómetros incluidos en el precio.',
                   '**Tipo de Tarifa**: Estándar. Con **más de 29 días** pasa sola a FLEXIRENT ([[reservar-flexirent]]).',
                   '**Tarifa (€/día)**: el precio por día que va a pagar. Compruébalo antes de seguir.'],
           marks=[[g.label('selected_category_id'), g.field('selected_category_id')],
                  [g.label('duration_range'), g.field('duration_range')],
                  [g.label('km_range'), g.field('km_range')],
                  [g.label('pricing_type'), g.field('pricing_type')],
                  [g.field('calculated_price')]],
           crop=modal(),
           warn='Si **Tarifa (€/día)** sale **0,00**, esa combinación no tiene precio (por ejemplo 100 Km solo existe para 4 horas). Cambia el **Rango de Km** hasta que salga un precio. Si reservas con 0,00 te saldrá el error «El precio por día debe ser mayor que cero».')
    row = g.page.locator('.modal-content .o_data_row', has_text='0777')
    g.step('Abajo salen **solo las furgonetas libres** esas fechas. Pulsa **Reservar** en la que quieras.',
           labels=['Mira la **Delegación** (dónde está la furgoneta) y la **Compañía** (de quién es).',
                   'Pulsa **Reservar** en esa fila.'],
           marks=[row.locator('td[name=delegation_id], td[name=company_id]'), row.locator('button', has_text='Reservar')],
           crop=modal(),
           tip='¿Buscas un modelo concreto? Escribe la marca o el modelo en **Buscar vehículo**. ¿Solo las de una oficina? Elige la **Delegación**.')
    row.locator('button', has_text='Reservar').click()
    g.wait(1500)
    g.step('Ya tienes el contrato en **Borrador**. Revisa cliente, furgoneta, fechas y precio.',
           marks=[g.page.locator('.o_statusbar_status')])
