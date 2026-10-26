from ._config import ADMIN, open_list, open_record, search

TASK = dict(
    id='seguros',
    title='Tarifas de seguros: qué cuesta el seguro sin franquicia',
    short='Seguros',
    cat='config',
    summary='Las **Tarifas de Seguros** dan el precio por día del seguro según el **tipo de seguro**, los **días** y el **tipo de conductor** (normal, o especial si tiene menos de 25 o más de 60 años).',
    when='Un cliente pregunta cuánto cuesta quitar la franquicia, o vas a cambiar el precio del seguro.',
    before=[ADMIN],
    tags=['seguro', 'franquicia', 'sin franquicia', 'seguro basico', 'conductor joven', 'menor de 25', 'mayor de 60', 'precio seguro'],
    result='Sabes qué precio por día se suma al contrato al elegir **Sin Franquicia**.',
    notes=['El **Seguro Básico** lleva una franquicia de **750 € + IVA**: si hay un daño, el cliente paga hasta esa cantidad.',
           'El tipo de conductor sale solo de la fecha de nacimiento del conductor ([[nuevo-cliente]]).',
           'Para cambiar precios, igual que en [[tarifas]]: no edites, crea una nueva con fecha **Vigente desde**.'],
    next=['revisar-contrato', 'tarifas'],
)


def run(g):
    open_list(g, 'Tarifas de Seguros', 'Pulsa el **+** del menú y luego **Tarifas de Seguros**.')
    search(g, 'Sin Franquicia')
    rows = g.page.locator('.o_data_row')
    g.step('Cada fila es un precio por día: tipo de seguro, días y tipo de conductor.', marks=[rows.first, rows.nth(1)], crop='top',
           labels=['Conductor **Normal**.', 'Conductor **Especial** (menos de 25 o más de 60 años): es más caro.'])
    open_record(g, rows.first)
    g.step('Dentro de una tarifa:',
           labels=['**Tipo de seguro**.', '**Duración** (tramo de días).', '**Tipo de conductor**.', '**Precio por día** con IVA.'],
           marks=[g.field('insurance_type'), g.field('duration_range'), g.field('driver_type'), g.field('price_per_day')],
           crop=g.page.locator('.o_form_sheet').first)
