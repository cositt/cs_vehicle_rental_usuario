from ._config import ADMIN, open_list, open_record, search

TASK = dict(
    id='reglas-deposito',
    title='Reglas de depósito: de dónde sale la fianza',
    short='Reglas de depósito',
    cat='config',
    summary='La **fianza** de cada contrato sale de las **Reglas de Depósitos**: según el **tipo** de furgoneta y cómo paga el cliente (**tarjeta de crédito**, débito o **efectivo**).',
    when='Un cliente pregunta cuánta fianza tiene que dejar, o el responsable quiere cambiarla.',
    before=[ADMIN],
    tags=['fianza', 'deposito', 'garantia', 'efectivo', 'tarjeta', 'credito', 'debito', 'cuanto de fianza'],
    warn='Con **efectivo** la fianza es más alta y el seguro **sin franquicia** es obligatorio: si no, el contrato no se puede entregar.',
    result='Sabes qué fianza se cobrará en cada caso.',
    notes=['La regla puede ser un importe **fijo**, un **porcentaje** del alquiler, o las dos cosas, con un mínimo y un máximo.'],
    next=['revisar-contrato', 'devolver-fianza'],
)


def run(g):
    open_list(g, 'Reglas de Depósitos', 'Pulsa el **+** del menú y luego **Reglas de Depósitos**.')
    search(g, 'Tipo D')
    rows = g.page.locator('.o_data_row')
    g.step('Escribe el tipo de furgoneta. Hay una regla por cada forma de pago.', marks=[rows.first], crop='top')
    open_record(g, rows.first)
    g.step('Dentro de una regla:',
           labels=['**Tipo de vehículo**.', '**Tipo de tarjeta** (crédito, débito o efectivo).', '**Importe fijo** de la fianza.',
                   'Mínimo y máximo.'],
           marks=[g.field('vehicle_category_id'), g.field('card_type'), g.field('deposit_fixed'),
                  [g.field('min_deposit'), g.field('max_deposit')]],
           crop=g.page.locator('.o_form_sheet').first)
