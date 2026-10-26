TASK = dict(
    id='revisar-contrato',
    title='Revisar y completar el contrato antes de entregar',
    short='Revisar el contrato',
    cat='reservas',
    summary='Antes de dar las llaves, repasa el contrato de arriba abajo: conductor, seguro, combustible, precio, forma de pago y fianza.',
    when='Justo después de reservar, o cuando el cliente viene a recoger la furgoneta.',
    before=['El contrato está en **Borrador** (si ya está «En curso», hay cosas que no se pueden cambiar).',
            'Tienes a mano el DNI y el carnet de conducir de quien va a conducir.'],
    tags=['completar contrato', 'editar contrato', 'conductor', 'seguro', 'combustible', 'forma de pago', 'fianza', 'tarjeta', 'efectivo'],
    result='El contrato está completo y guardado, listo para entregar.',
    next=['entregar', 'imprimir-enviar'],
)


def run(g):
    g.open_app()
    g.step('Pulsa **Contratos** en el menú y abre el contrato del cliente.', marks=[g.menu('Contratos')], crop='top')
    g.go('Contratos')
    row = g.page.locator('.o_data_row').first
    g.step('Pulsa en la línea del contrato para abrirlo. Arriba puedes buscar por cliente o matrícula.',
           marks=[row, g.page.locator('.o_searchview')])
    g.open_row(row)
    sheet = g.scope()
    g.step('Comprueba los **datos del cliente**: se rellenan solos desde su ficha y salen en el contrato impreso.',
           labels=['**DNI/NIE** (o CIF si es empresa). Pon la **caducidad del DNI** si la tienes.', '**Domicilio** completo.'],
           marks=[[g.label('customer_dni'), g.field('customer_dni'), g.field('customer_dni_expiry_date')],
                  [g.label('customer_address'), g.field('customer_address')]],
           crop=g.band(g.sep('DETALLES DEL CLIENTE'), g.field('customer_address')),
           tip='Si falta algo, escríbelo aquí; lo que escribas no se pisa. Para que salga bien la próxima vez, corrígelo en la ficha del cliente ([[nuevo-cliente]]).')
    g.m2o('authorized_driver_id', 'Pepe Demo')
    g.step('Elige el **Conductor** que va a llevar la furgoneta. El carnet y sus fechas se rellenan solos desde su ficha.',
           labels=['**Conductor**: escribe el nombre y elígelo.',
                   'Comprueba que el **carnet no está caducado**.'],
           marks=[[g.label('authorized_driver_id'), g.field('authorized_driver_id')],
                  [g.field('driver_license_number'), g.field('driver_license_expiry_date')]],
           crop=g.band(g.sep('CONDUCTOR AUTORIZADO'), g.field('driver_license_expiry_date')),
           warn='Si el **carnet o el DNI caducan antes de la devolución**, sale un aviso y una franja roja. Pide el documento en vigor antes de dar las llaves. Si dejas el conductor vacío, al entregar te preguntará si quieres **Entregar sin conductor**.')
    g.select('insurance_type', 'Sin Franquicia')
    g.step('Elige el **seguro** que ha contratado el cliente. El precio por día y el total se calculan solos.',
           labels=['**Tipo de Seguro**: Básico (va **incluido en la tarifa**, franquicia 750 € + IVA por impacto) o Sin Franquicia (se cobra por día).',
                   '**Conductor Especial**: márcalo si el conductor tiene menos de 25 o más de 60 años (sube el precio).',
                   'Precio por día y total del seguro.'],
           marks=[[g.label('insurance_type'), g.field('insurance_type')],
                  [g.label('driver_special'), g.field('driver_special')],
                  [g.field('insurance_price_per_day'), g.field('total_insurance_cost')]],
           crop=g.band(g.sep('SEGURO Y COBERTURA'), g.field('driver_special')),
           stop='Si el cliente **paga en efectivo**, el seguro **Sin Franquicia es obligatorio**. Si no lo pones, no te dejará entregar.')
    g.step('Revisa **fechas y oficinas**: dónde recoge y dónde devuelve.',
           labels=['**Recogida**: oficina donde se lleva la furgoneta.',
                   '**Entrega**: oficina donde la va a devolver. Si es otra distinta, hay recargo.'],
           marks=[[g.label('pick_up_delegation_id'), g.field('pick_up_delegation_id')],
                  [g.label('drop_off_delegation_id'), g.field('drop_off_delegation_id')]],
           crop=g.band(g.sep('DETALLES DE RECOGIDA'), g.field('drop_off_delegation_id')))
    g.select('initial_fuel_level', 'Lleno')
    g.step('En **Detalles del vehículo**, apunta cómo sale la furgoneta.',
           labels=['**Último odómetro**: los km que marca ahora.',
                   '**Combustible en Entrega**: sale **Lleno**, que es lo normal. Cámbialo solo si sale con menos.'],
           marks=[[g.label('last_odometer'), g.field('last_odometer')],
                  [g.label('initial_fuel_level'), g.field('initial_fuel_level')]],
           crop=g.band(g.sep('DETALLES DEL VEHÍCULO'), g.field('is_scratch_report')),
           tip='¿Te has equivocado de furgoneta? Mientras esté en Borrador puedes cambiar el **Vehículo** aquí mismo.')
    g.step('Revisa el **precio**: tarifa, kilómetros incluidos y total.',
           labels=['Tarifa y kilómetros incluidos.', '**Alquiler / Día** y **Total Renta del Vehículo**.'],
           marks=[[g.field('km_range'), g.field('duration_range')],
                  [g.field('rent'), g.field('total_vehicle_rent')]],
           crop=g.band(g.sep('DETALLES DEL ALQUILER'), g.field('tax_ids')),
           warn='Si cambias el precio a mano, te pedirá **el motivo del cambio**. Escríbelo: queda registrado.')
    g.radio('payment_type', 'Pago completo')
    g.radio('deposit_card_type', 'Crédito')
    g.step('Elige **cómo paga** y **con qué tarjeta deja la fianza**:',
           labels=['**Tipo de pago**: sale **Pago completo** (todo de una vez). Cámbialo solo si paga por cuotas (semanal, mensual…).',
                   '**Tipo de Tarjeta para Depósito**: crédito, débito o efectivo. Cambia el importe de la fianza.',
                   '**Depósito**: importe de la fianza que se le cobra. Sale de las [[reglas-deposito|Reglas de Depósitos]].'],
           marks=[[g.label('payment_type'), g.field('payment_type')],
                  [g.label('deposit_card_type'), g.field('deposit_card_type')],
                  [g.field('calculated_deposit'), g.field('deposit')]],
           crop=g.band(g.sep('DETALLES DEL PAGO'), g.field('deposit')))
    save = g.page.locator('.o_form_button_save:visible')
    g.step('Pulsa **Guardar** (la nube de arriba). Si no hay nube, ya está guardado.', marks=[save], crop='top')
    g.save()
