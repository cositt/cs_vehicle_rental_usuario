TASK = dict(
    id='menu',
    title='Moverse por el menú de Alquiler de vehículos',
    short='El menú',
    cat='empezar',
    summary='Todo el trabajo diario está en la aplicación **Alquiler de vehículos**. Este es el mapa del menú de arriba.',
    when='Primer día, o cuando no encuentres algo.',
    before=['Has entrado en Odoo.'],
    tags=['menu', 'donde esta', 'aplicacion', 'inicio', 'entrar', 'navegar', 'mapa'],
    result='Sabes dónde está cada cosa.',
    next=['panel', 'disponibilidad', 'reservar'],
)


def run(g):
    g.home()
    g.step('En la pantalla de inicio, pulsa **Alquiler de vehículos**.', marks=[g.page.locator('.o_app', has_text='Alquiler de vehículos')], crop='top')
    g.open_app()
    nav = g.page.locator('.o_menu_sections')
    items = ['Panel', 'Consultas de Reserva', 'Disponibilidad', 'Reservar Vehículo', 'Reserva Múltiple', 'Vehículos Totales',
             'Contratos', 'Contratos Grupo', 'Ampliaciones', 'Clientes']
    g.step('Este es el menú de arriba:', crop='top',
           marks=[nav.locator('.o_nav_entry, .dropdown-toggle', has_text=t).first for t in items],
           labels=['**Panel**: resumen con números del día.', '**Consultas de Reserva**: lo que llega de la web.',
                   '**Disponibilidad**: qué furgonetas están libres u ocupadas.', '**Reservar Vehículo**: hacer una reserva (lo más usado).',
                   '**Reserva Múltiple**: varias furgonetas de una vez.', '**Vehículos Totales**: la flota.',
                   '**Contratos**: todos los contratos.', '**Contratos Grupo**: contratos de varias furgonetas juntas.',
                   '**Ampliaciones**: días extra.', '**Clientes**: fichas de clientes y conductores.'])
    more = g.page.locator('.o_menu_sections .o_menu_sections_more, .o_menu_sections .dropdown-toggle:has(.fa-plus), .o_menu_sections button:has-text("+")').last
    if more.count():
        more.click()
        g.wait(600)
        dd = g.page.locator('.o-dropdown--menu').last
        g.step('Pulsando el **+** salen el resto: Solicitudes de mantenimiento, Sustituciones, Devoluciones, Tarifas, Reglas de Depósitos y **Configuraciones**.',
               marks=[more], crop=dd,
               tip='Si tu pantalla es más ancha verás más opciones directamente en la barra, sin el **+**.')
        g.page.keyboard.press('Escape')
