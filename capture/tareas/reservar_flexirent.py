from datetime import date, timedelta

TASK = dict(
    id='reservar-flexirent',
    title='Reservar para más de un mes (FLEXIRENT)',
    short='Reserva larga (FLEXIRENT)',
    cat='reservas',
    summary='Para alquileres de **más de 29 días** se usa la tarifa FLEXIRENT: una **cuota mensual** según los kilómetros al mes que necesite el cliente. El asistente la elige solo al poner los días.',
    when='Un cliente quiere la furgoneta uno, dos o más meses.',
    before=['El cliente ya existe en **Clientes**.',
            'Sabes cuántos **kilómetros al mes** va a hacer (3.000, 5.000 o 7.500).'],
    tags=['flexirent', 'larga temporada', 'larga duracion', 'meses', 'mensual', 'cuota', '60 dias', '30 dias', 'renting', 'alquiler largo'],
    result='Contrato en **Borrador** con tarifa FLEXIRENT, el paquete de km y la **cuota mensual**. El pago sale **Mensual**.',
    notes=['La fianza de FLEXIRENT es siempre de **750 €** ([[reglas-deposito]]).',
           'Los km que pase del paquete se cobran aparte al devolver.'],
    next=['revisar-contrato', 'cobrar-cuotas'],
)


def d(days, hour='09:00:00'):
    return (date.today() + timedelta(days=days)).strftime('%d/%m/%Y ') + hour


def run(g):
    g.open_app()
    g.go('Reservar Vehículo')
    modal = lambda: g.page.locator('.modal-content').last
    g.m2o('customer_id', 'Cliente Demo')
    g.fill('start_date', d(10))
    g.fill('rental_days', '60')
    g.m2o('selected_category_id', 'Tipo D')
    g.step('En **Reservar Vehículo** pon cliente, fecha de inicio y **Nº de días** (60). Con más de 29 días, el **Tipo de Tarifa** pasa solo a **FLEXIRENT**.',
           labels=['**Cliente** y **fecha de inicio**.', '**Nº de días**: la fecha final se calcula sola.', '**Tipo de Tarifa**: FLEXIRENT.'],
           marks=[[g.field('customer_id'), g.field('start_date')], [g.field('rental_days'), g.field('end_date')],
                  [g.label('pricing_type'), g.field('pricing_type')]],
           crop=modal(),
           tip='No hace falta elegir duración ni rango de km: en FLEXIRENT no se usan.')
    g.select('flexirent_km_package', '5.000')
    g.step('Elige el **Paquete de km** al mes. La **cuota mensual** cambia según el paquete.',
           labels=['**Paquete de km**: 3.000, 5.000 o 7.500 km cada 30 días.', '**Cuota mensual** (IVA incluido).'],
           marks=[[g.label('flexirent_km_package'), g.field('flexirent_km_package')],
                  g.field('calculated_price')],
           crop=modal())
    row = g.page.locator('.modal-content .o_data_row', has_text='0888')
    g.step('Pulsa **Reservar** en la furgoneta que quieras.', marks=[row.locator('button', has_text='Reservar')], crop=modal())
    row.locator('button', has_text='Reservar').click()
    g.wait(2000)
    g.step('El contrato sale con la tarifa **FLEXIRENT**, el paquete de km y la **cuota mensual**. Revísalo como cualquier otro ([[revisar-contrato]]).',
           labels=['Tarifa **FLEXIRENT**.', '**Paquete de km** y **cuota mensual**.', 'Mensualidades y **total**.'],
           marks=[g.field('pricing_type'), [g.field('flexirent_km_package'), g.field('rent')],
                  [g.field('flexirent_months'), g.field('total_vehicle_rent')]],
           crop=g.band(g.sep('DETALLES DEL ALQUILER'), g.field('total_vehicle_rent')))
