TASK = dict(
    id='sustituir',
    title='Cambiar la furgoneta durante el alquiler (sustitución)',
    short='Sustituir furgoneta',
    cat='durante',
    summary='Si la furgoneta se avería, tiene un golpe o el cliente necesita otra, se cambia por otra sin cerrar el contrato. Son 4 pasos guiados.',
    when='Avería, accidente, o el cliente pide otro tamaño a mitad del alquiler.',
    before=['El contrato está **En curso**.',
            'Tienes delante las dos furgonetas: la que se retira y la nueva (km y combustible de cada una).'],
    tags=['sustituir', 'sustitucion', 'cambiar furgoneta', 'cambio de vehiculo', 'averia', 'otra furgoneta', 'reemplazar', 'addendum'],
    result='El contrato sigue **En curso** con la furgoneta nueva. La vieja queda libre (o en taller) y se genera el **addendum** para firmar.',
    notes=[['tip', '¿La vieja va al taller? Después pásala a mantenimiento: [[mantenimiento]].']],
    next=['mantenimiento', 'devolver'],
)


def run(g):
    cid = g.new_contract('1221-DMO', 'María Ejemplo López', start_in=-2, days=6, driver='María Ejemplo López')
    g.open_contract(cid)
    g.step('En el contrato **En curso**, pulsa **Sustituir Vehículo**.', marks=[g.button(name='action_open_substitution_wizard')], crop='top')
    g.button(name='action_open_substitution_wizard').click()
    g.page.wait_for_selector('.o_field_widget[name=old_vehicle_odometer]', timeout=30000)
    g.wait(1000)
    sheet = lambda: g.page.locator('.o_form_sheet, .o_form_renderer').first
    odo = g.find('fleet.vehicle', [['license_plate', '=', '1221-DMO']], ('odometer',))['odometer']
    g.fill('old_vehicle_odometer', str(int(odo) + 380))
    g.radio('old_vehicle_fuel_level', '3/4')
    g.step('**Paso 1 de 4 — la furgoneta que se retira.** Apunta cómo vuelve y pulsa **Siguiente**.',
           labels=['**Kilometraje** que marca ahora.', '**Combustible** con el que vuelve.',
                   '**¿Tiene daños?** Márcalo si vuelve con golpes: podrás pintarlos y facturarlos.', '**Siguiente**.'],
           marks=[[g.label('old_vehicle_odometer'), g.field('old_vehicle_odometer')], [g.label('old_vehicle_fuel_level'), g.field('old_vehicle_fuel_level')],
                  [g.label('old_vehicle_has_damage'), g.field('old_vehicle_has_damage')], g.button(name='action_next_step')])
    g.button(name='action_next_step').click()
    g.wait(1500)
    g.radio('reason', 'Avería del Vehículo')
    g.fill('reason_notes', 'Ruido en el embrague')
    g.m2o('new_vehicle_id', '1887')
    g.step('**Paso 2 — motivo y furgoneta nueva.**',
           labels=['**Motivo** de la sustitución (obligatorio).', 'Notas: explica qué pasa.', '**Vehículo Sustituto**: solo salen las **libres** esas fechas.',
                   'Comparativa de las dos furgonetas. Pulsa **Siguiente**.'],
           marks=[[g.label('reason'), g.field('reason')], g.field('reason_notes'), [g.label('new_vehicle_id'), g.field('new_vehicle_id')],
                  g.button(name='action_next_step')],
           warn='Si eliges una furgoneta de **otra categoría**, puede haber **diferencia de precio**. Lo verás en el paso 4.')
    g.button(name='action_next_step').click()
    g.wait(1500)
    g.radio('new_vehicle_fuel_level', 'Lleno')
    g.step('**Paso 3 — la furgoneta nueva.** Apunta sus km y combustible al salir. Si ya tiene algún golpe, márcalo en **Daños Previos** para que no se le cobre al cliente.',
           marks=[[g.label('new_vehicle_odometer'), g.field('new_vehicle_odometer')], [g.label('new_vehicle_fuel_level'), g.field('new_vehicle_fuel_level')],
                  [g.label('new_vehicle_has_damage'), g.field('new_vehicle_has_damage')], g.button(name='action_next_step')],
           labels=['Km al salir.', 'Combustible al salir.', 'Daños que ya tenía.', '**Siguiente**.'])
    g.button(name='action_next_step').click()
    g.wait(1500)
    g.step('**Paso 4 — resumen.** Revisa las dos furgonetas y, si las hay, la **diferencia de precio**.',
           labels=['Furgoneta que se retira.', 'Furgoneta que se entrega.', 'Diferencia de precio por día (si cambia de categoría).'],
           marks=[g.field('old_vehicle_odometer'), g.field('new_vehicle_odometer'), g.field('price_difference')],
           detail='Marca **aplicar diferencia** si el cliente paga (o recibe) la diferencia. Después podrás facturarla desde la sustitución.')
    g.sign('customer_signature')
    g.sign('company_signature')
    g.step('Que firme el cliente, firma tú y pulsa **Confirmar Sustitución**.',
           marks=[[g.field('customer_signature'), g.field('company_signature')], g.button(name='action_confirm_substitution')])
    g.button(name='action_confirm_substitution').click()
    g.wait(2500)
    g.step('Hecho: el contrato sigue **En curso** con la **furgoneta nueva**. En el historial de la derecha tienes el **Addendum** para imprimirlo o enviarlo.',
           labels=['Botón **Sustituciones**: el historial de cambios del contrato.', 'Mensaje con el resumen y el PDF del addendum.'],
           marks=[g.page.locator('button[name=action_view_substitutions]'), g.page.locator('.o-mail-Message').first])
