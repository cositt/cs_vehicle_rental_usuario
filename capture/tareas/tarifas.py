from datetime import date

from ._config import ADMIN, open_list, open_record, search

TASK = dict(
    id='tarifas',
    title='Tarifas de alquiler: consultarlas y subir precios para la nueva temporada',
    short='Tarifas',
    cat='config',
    summary='Las **Tarifas de Vehículos** dan el precio por día según el **tipo** de furgoneta, los **días** y los **km**. Para cambiar precios no se toca la tarifa vieja: se **duplica con nuevas fechas** y a partir de ese día se usa la nueva sola.',
    when='Quieres saber cuánto cuesta un alquiler, o vas a cambiar precios (por ejemplo, el 1 de enero).',
    before=[ADMIN],
    tags=['precio', 'precios', 'tarifa', 'tarifas', 'subir precios', 'nueva temporada', 'temporada', 'cuanto cuesta', 'precio por dia', 'flexirent', 'duplicar'],
    stop='**No cambies el precio** de una tarifa que ya está en uso: cambiarías el precio de los contratos que se recalculen. Duplícala con una fecha **Vigente desde** nueva.',
    result='La nueva tarifa entra sola el día de **Vigente Desde**. Hasta entonces se sigue usando la vieja.',
    notes=['Los precios llevan el **IVA incluido**. La columna **Sin IVA** se calcula sola.',
           'Si una combinación (tipo + días + km) no tiene tarifa, al reservar sale **Tarifa 0,00**.'],
    next=['reservar', 'seguros'],
)


def run(g):
    open_list(g, 'Tarifas de Vehículos', 'Pulsa el **+** del menú y luego **Tarifas de Vehículos**.')
    search(g, 'Tipo D')
    rows = g.page.locator('.o_data_row', has_text='3-5')
    g.step('Escribe el tipo (por ejemplo «Tipo D») en el buscador. Cada fila es un precio por día para unos días y unos km.',
           labels=['El buscador.', 'Una tarifa: tipo, duración, km y **Precio/Día**.'],
           marks=[g.page.locator('.o_searchview').first, g.page.locator('.o_data_row').nth(3)], crop='top',
           tip='Con el filtro **Vigentes Hoy** ves solo los precios que se aplican hoy.')
    open_record(g, rows.first)
    g.step('Abre una tarifa. Lo que tiene:',
           labels=['**Tipo de vehículo** y **Tipo** (Estándar o FLEXIRENT).', '**Vigencia**: desde y hasta qué día vale.',
                   '**Rango de km** y **Duración**.', '**Precio por día** con IVA.'],
           marks=[[g.field('vehicle_category_id'), g.field('pricing_type')], [g.field('valid_from'), g.field('valid_until')],
                  [g.field('km_range'), g.field('duration_range')], g.field('price_per_unit')],
           crop=g.page.locator('.o_form_sheet').first)
    dup = g.button(name='action_duplicate_with_new_dates')
    g.step('Para un precio nuevo pulsa **Duplicar con Nuevas Fechas**.', marks=[dup], crop='top')
    dup.click()
    g.page.wait_for_selector('.modal-content .o_field_widget[name=valid_from]', timeout=20000)
    g.wait(900)
    modal = g.page.locator('.modal-content').last
    g.fill('valid_from', f'01/01/{date.today().year + 1}')
    g.fill('price_per_unit', '90,00')
    g.step('Se abre una copia con el mismo tipo, días y km. Pon la fecha **Vigente desde** y el **precio nuevo**, y guarda.',
           labels=['**Vigente desde**: el día que empieza el precio nuevo.', '**Precio por día** nuevo (con IVA).', '**Guardar**.'],
           marks=[modal.locator('[name=valid_from]').first, modal.locator('[name=price_per_unit]').first, modal.locator('.modal-footer button').first],
           crop=modal,
           warn='Repite con **cada** combinación que cambie de precio. Las que no dupliques siguen con el precio viejo.')
    modal.locator('.modal-footer button').first.click()
    g.wait(1500)
