TASK = dict(
    id='panel',
    title='El Panel: los números del día',
    short='Panel',
    cat='empezar',
    summary='El Panel enseña de un vistazo cuántas furgonetas hay, cuántas están en taller, contratos en curso, devueltos y facturas pendientes. Cada cuadro se puede pulsar.',
    when='Al empezar el día, para saber cómo está todo.',
    before=['Tienes las dos compañías marcadas ([[companias]]).'],
    tags=['panel', 'dashboard', 'resumen', 'estadisticas', 'numeros', 'inicio'],
    result='Sabes cuántas furgonetas hay libres, en taller y alquiladas, y qué facturas faltan por cobrar.',
    next=['disponibilidad'],
)


def run(g):
    g.open_app()
    g.go('Panel')
    g.wait(1500)
    cards = g.page.locator('.o_action_manager .card, .o_action_manager [class*=card]')
    g.step('Arriba, las **estadísticas actuales**. Pulsa cualquier cuadro para ver la lista.',
           labels=['**Vehículos Totales** y **Operacionales** (los que se pueden alquilar).', '**Mantenimiento**: en el taller.',
                   '**Facturas Pendientes**: por cobrar.'],
           marks=[g.page.locator('.o_action_manager', has_text='Vehículos Totales').locator('text=Vehículos Totales').first,
                  g.page.locator('.o_action_manager').locator('text=Mantenimien').first,
                  g.page.locator('.o_action_manager').locator('text=Facturas').last])
    g.page.locator('.o_action_manager').locator('text=Detalles de Contratos').first.evaluate("e => e.scrollIntoView({block: 'start'})")
    g.wait(600)
    g.step('Más abajo, los **contratos** por estado (En curso, Devuelto, Cancelado) y las gráficas de duración e ingresos.')
