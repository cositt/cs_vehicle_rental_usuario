TASK = dict(
    id='ficha-vehiculo',
    title='La ficha de una furgoneta: qué mirar',
    short='Ficha de furgoneta',
    cat='flota',
    summary='Cada furgoneta tiene su **ficha** con la matrícula, de qué compañía es, en qué delegación está, si está operativa o en el taller, y todos sus contratos.',
    when='Quieres saber dónde está una furgoneta, de quién es o qué contratos ha tenido.',
    before=[],
    tags=['vehiculo', 'furgoneta', 'ficha', 'matricula', 'flota', 'delegacion', 'kilometros', 'odometro', 'vehiculos'],
    warn='No cambies la **Compañía** ni la **Delegación** de una furgoneta sin avisar al responsable: de la compañía depende quién factura sus contratos.',
    result='Sabes de quién es la furgoneta, dónde está y si se puede alquilar.',
    next=['mantenimiento-vehiculo', 'disponibilidad'],
)


def run(g):
    g.open_app()
    g.step('Pulsa **Vehículos Totales** en el menú.', marks=[g.menu('Vehículos Totales')], crop='top')
    g.go('Vehículos Totales')
    g.page.wait_for_selector('.o_kanban_record', timeout=30000)
    g.wait(800)
    search = g.page.locator('.o_searchview input').first
    search.fill('0111')
    search.press('Enter')
    g.wait(1500)
    card = g.page.locator('.o_kanban_record', has_text='0111').first
    g.step('Escribe la **matrícula** (o parte) en el buscador y pulsa Intro. Abre la furgoneta.',
           marks=[g.page.locator('.o_searchview').first, card], crop='top')
    card.click()
    g.page.wait_for_selector('.o_form_view .o_field_widget[name=license_plate]', timeout=30000)
    g.wait(1200)
    g.step('Esta es la ficha. Lo importante:',
           labels=['Cinta **Operacional** (se puede alquilar) o **En Mantenimiento** (en el taller, no sale en las reservas).',
                   '**Matrícula**.',
                   '**Compañía**: de quién es la furgoneta. Sus contratos y facturas van a esa compañía.',
                   '**Delegación**: la oficina donde está ahora.',
                   '**Contratos de alquiler**: pulsa para ver todos los suyos.'],
           marks=[g.page.locator('.ribbon').first, g.field('license_plate'), g.field('company_id'),
                  g.field('delegation_id'), g.button(name='action_rental_contract_view')],
           crop=g.page.locator('.o_form_sheet').first,
           detail='La delegación cambia sola cuando la furgoneta se devuelve en otra oficina.')
    g.step('Más abajo: **cuentakilómetros**, tipo de combustible y el **Horario de Mantenimiento** (cada cuántos días va a revisión).',
           marks=[g.field('odometer'), g.field('maintenance_schedule_id')],
           crop=g.band(g.field('odometer'), g.field('maintenance_schedule_id')))
