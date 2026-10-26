TASK = dict(
    id='disponibilidad',
    title='Ver qué furgonetas están ocupadas (Disponibilidad)',
    short='Disponibilidad',
    cat='empezar',
    summary='Un calendario con una barra por cada contrato: de qué fecha a qué fecha está ocupada cada furgoneta.',
    when='Para ver de un vistazo la ocupación de la flota, o antes de ampliar un alquiler.',
    before=['Tienes las dos compañías marcadas ([[companias]]).'],
    tags=['disponibilidad', 'libre', 'libres', 'ocupada', 'calendario', 'gantt', 'que hay', 'hay furgonetas', 'ocupacion'],
    result='Sabes qué furgonetas están ocupadas y hasta cuándo.',
    notes=[['tip', 'Para saber qué furgonetas están **libres** en unas fechas concretas, lo más rápido es el asistente [[reservar]]: solo te enseña las libres.']],
    next=['reservar', 'ampliar'],
)


def run(g):
    g.open_app()
    g.step('Pulsa **Disponibilidad** en el menú.', marks=[g.menu('Disponibilidad')], crop='top')
    g.go('Disponibilidad')
    g.page.wait_for_selector('.gantt_row_task', timeout=30000)
    g.wait(1500)
    chart = g.page.locator('#availibilityChart')
    g.step('Cada **fila** es una furgoneta con contrato, y cada **barra** es el tiempo que está alquilada.',
           labels=['Furgoneta, fecha de inicio, fecha de fin y días.', 'La barra de cada contrato, con su número.', 'Las fechas, de izquierda a derecha.'],
           marks=[g.page.locator('.gantt_grid_data').first, g.page.locator('.gantt_task_line').first, g.page.locator('.gantt_task_scale').first],
           crop=g.band(g.page.locator('.vehicle_rental_dashboard h4').first, g.page.locator('.gantt_row_task').last) if False else None,
           detail='Las furgonetas que **no salen** en la lista no tienen ningún contrato: están libres.')
