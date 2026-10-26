from ._config import ADMIN, open_list, open_record

TASK = dict(
    id='politicas',
    title='Políticas de cancelación',
    short='Políticas de cancelación',
    cat='config',
    summary='Las **Políticas de Cancelación** son los textos que se eligen al [[cancelar]] un contrato: gratis con más de 48 h, con cargo con menos de 48 h, o «No presentado».',
    when='Vas a cancelar y no sabes qué política elegir, o el responsable quiere cambiar el texto.',
    before=[ADMIN],
    tags=['cancelacion', 'politica', 'anular', 'no presentado', 'no show', '48 horas', 'condiciones cancelacion'],
    result='Sabes qué política aplicar en cada cancelación.',
    notes=['Hay una política igual para cada compañía (Sunset y Pinveco). Se usa la de la compañía del contrato.'],
    next=['cancelar'],
)


def run(g):
    open_list(g, 'Política de cancelación', 'Pulsa el **+** del menú y, en **Configuraciones**, **Política de cancelación**.')
    rows = g.page.locator('.o_data_row')
    g.step('Estas son las políticas. Cada una con su compañía.', marks=[rows.first, rows.nth(1), rows.nth(2)], crop='top',
           labels=['**Gratuita**: cancela con más de 48 h. Sin cargo.', '**Menos de 48 h**: se cobra un cargo.', '**No presentado**: no vino a recogerla.'])
    open_record(g, rows.nth(1))
    g.step('Dentro está el **texto** que verá el cliente.', marks=[g.field('title'), g.field('terms_and_conditions')],
           crop=g.page.locator('.o_form_sheet').first)
