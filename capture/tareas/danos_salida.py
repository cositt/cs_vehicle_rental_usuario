TASK = dict(
    id='danos-salida',
    title='Marcar los golpes que ya tiene la furgoneta al entregarla',
    short='Daños a la salida',
    cat='entrega',
    summary='Antes de dar las llaves, da una vuelta a la furgoneta **con el cliente** y marca en el dibujo los golpes y rayones que **ya tiene**. Así, a la vuelta, no se le cobra al cliente algo que no hizo, ni se nos escapa algo que sí hizo.',
    when='Justo antes de entregar la furgoneta ([[entregar]]).',
    before=['El contrato está en **Borrador**.', 'El cliente está contigo delante de la furgoneta.'],
    tags=['golpes', 'rayones', 'daños', 'arañazos', 'bollos', 'revisar furgoneta', 'salida', 'estado', 'dibujo', 'croquis', 'danos previos'],
    stop='Si no marcas un golpe que ya estaba, a la vuelta **no podrás demostrar** quién lo hizo. Marca **todo**, aunque sea pequeño.',
    result='El dibujo con los daños queda en la pestaña **Daños del Vehículo** del contrato.',
    notes=['Haz también **fotos** de los golpes y súbelas en la pestaña **Imágenes de vehículos**.'],
    next=['entregar', 'danos-devolucion'],
)


def run(g):
    g.open_contract(g.find('vehicle.contract', [['vehicle_id.license_plate', '=', '0777-DMO']])['id'])
    tab = g.page.locator('.o_notebook a.nav-link[name=vehicle_damage_painting]').first
    tab.click()
    g.wait(600)
    btn = g.button(name='open_damage_painter')
    g.step('En el contrato abre la pestaña **Daños del Vehículo** y pulsa **Abrir Editor de Daños**.',
           marks=[tab, btn], crop=g.band(tab, btn))
    btn.click()
    g.page.wait_for_selector('.modal-content canvas', timeout=20000)
    g.wait(2000)
    pm = g.page.locator('.modal-content').last
    canvas = pm.locator('canvas').first
    g.draw(canvas, [[(.62, .30), (.66, .27), (.70, .30), (.66, .34), (.62, .30)]])
    g.step('Pinta encima de cada golpe o rayón, en la vista que toque (frontal, laterales, techo y trasera).',
           labels=['Herramientas y colores.', 'Dibuja con el ratón (o el dedo en la tableta) sobre la furgoneta.', '**Guardar**.'],
           marks=[pm.locator('.damage_tool'), canvas, pm.locator('.o_save_damage_btn').first],
           crop=pm, tip='Con **Texto** puedes escribir al lado, por ejemplo «rayón 10 cm».')
    pm.locator('.o_save_damage_btn').first.click()
    g.page.wait_for_selector('.modal-content canvas', state='detached', timeout=20000)
    g.wait(1500)
    g.page.locator('.o_notebook a.nav-link[name=vehicle_damage_painting]').first.click()
    g.wait(600)
    g.step('Listo: el dibujo queda guardado en el contrato.', marks=[g.field('painted_damage_image')],
           crop=g.band(g.page.locator('.o_notebook a.nav-link[name=vehicle_damage_painting]').first, g.field('painted_damage_image')),
           detail='Al guardar, el editor se cierra solo y el dibujo aparece en el contrato. Si te equivocas, **Limpiar Imagen** lo borra y empiezas de nuevo.')
