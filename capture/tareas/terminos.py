from ._config import ADMIN, open_list, open_record

TASK = dict(
    id='terminos',
    title='Términos y condiciones del contrato',
    short='Términos',
    cat='config',
    summary='Los **Términos de Acuerdo de Alquiler** son las condiciones generales que salen impresas en el contrato. Hay unos por compañía.',
    when='Un cliente pregunta por una condición, o el responsable tiene que actualizar el texto.',
    before=[ADMIN],
    tags=['condiciones', 'terminos', 'clausulas', 'contrato', 'letra pequeña', 'condiciones generales'],
    stop='Estos textos son **legales**. No los cambies sin que lo apruebe el responsable o la asesoría.',
    result='Sabes dónde están las condiciones que firma el cliente.',
    next=['imprimir-enviar'],
)


def run(g):
    open_list(g, 'Términos de Acuerdo de Alquiler', 'Pulsa el **+** del menú y, en **Configuraciones**, **Términos de Acuerdo de Alquiler**.')
    rows = g.page.locator('.o_data_row')
    g.step('Una fila por compañía.', marks=[rows.first, rows.nth(1)], crop='top')
    open_record(g, rows.first)
    g.step('El texto completo. Es lo que sale en las últimas páginas del contrato impreso.',
           marks=[g.field('rental_terms')], crop='top')
