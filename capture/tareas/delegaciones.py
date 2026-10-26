from ._config import ADMIN, open_list, open_record

TASK = dict(
    id='delegaciones',
    title='Delegaciones (oficinas)',
    short='Delegaciones',
    cat='config',
    summary='Las **Delegaciones** son las oficinas donde se recogen y devuelven las furgonetas. Su dirección, teléfono, correo y horario salen en los correos al cliente.',
    when='Cambia el teléfono o el horario de una oficina, o quieres ver cuántas furgonetas tiene.',
    before=[ADMIN],
    tags=['delegacion', 'oficina', 'sucursal', 'horario', 'direccion oficina', 'telefono oficina', 'malaga', 'sevilla', 'cordoba'],
    warn='Revisa bien el **correo** y el **teléfono**: son los que ve el cliente en los correos de reserva y entrega.',
    result='Los datos de la oficina están al día.',
    next=['reservar', 'ficha-vehiculo'],
)


def run(g):
    open_list(g, 'Delegaciones', 'Pulsa el **+** del menú y, en **Configuraciones**, **Delegaciones**.')
    rows = g.page.locator('.o_data_row')
    g.step('Las oficinas, con el número de furgonetas que hay en cada una.', marks=[rows.first], crop='top')
    open_record(g, rows.filter(has_text='Málaga').first)
    g.step('Dentro: dirección, teléfono, correo y horario.',
           marks=[g.field('street'), [g.field('phone'), g.field('email')], g.field('schedule')],
           crop=g.page.locator('.o_form_sheet').first)
