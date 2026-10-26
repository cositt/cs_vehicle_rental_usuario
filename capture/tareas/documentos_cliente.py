import os

CARNET = os.path.join(os.path.dirname(__file__), '..', 'assets', 'carnet_ejemplo.png')

TASK = dict(
    id='documentos-cliente',
    title='Guardar el carnet y el DNI escaneados en el contrato',
    short='Documentos',
    cat='reservas',
    summary='Cada contrato tiene un botón **Documentos** para guardar la foto del carnet de conducir, el DNI o el pasaporte del cliente. Así, si hay una multa o un problema, la copia está a mano.',
    when='El cliente te da su carnet y su DNI al recoger la furgoneta.',
    before=['El contrato ya existe ([[reservar]]).', 'Tienes la foto o el escaneo del documento en el ordenador (JPG, PNG o PDF).'],
    tags=['documentos', 'carnet', 'dni', 'pasaporte', 'escanear', 'foto', 'adjuntar', 'subir archivo', 'permiso de conducir'],
    warn='Haz la foto **legible y entera**: que se lean el nombre, el número y las fechas. Una foto borrosa no sirve para una multa.',
    result='El botón **Documentos** del contrato muestra cuántos hay guardados.',
    notes=['Tipos que se usan: **Licencia de conducir** (carnet), **Pasaporte** y **Tarjeta de identificación con foto** (DNI o NIE). Los demás (Aadhaar, elector, racionamiento) son de otro país: no los uses.'],
    next=['imprimir-enviar', 'entregar'],
)


def run(g):
    g.open_contract(g.find('vehicle.contract', [['vehicle_id.license_plate', '=', '0777-DMO']])['id'])
    smart = g.button(name='action_customer_document')
    g.step('En el contrato, pulsa el botón **Documentos** (arriba a la derecha).', marks=[smart], crop='top')
    smart.click()
    g.page.wait_for_selector('.o_list_view', timeout=30000)
    g.wait(900)
    new = g.page.locator('.o_control_panel button', has_text='Nuevo').first
    g.step('Se abre la lista de documentos de este contrato (vacía la primera vez). Pulsa **Nuevo**.',
           marks=[new], crop='top')
    new.click()
    g.wait(1200)
    g.select('document_type', 'Licencia de conducir')
    g.page.locator('.o_data_row input[type=file]').first.set_input_files(CARNET)
    g.wait(1500)
    row = g.page.locator('.o_data_row').first
    g.step('Elige el **tipo** y sube el archivo.',
           labels=['**Tipo de documento**: *Licencia de conducir* = carnet.', '**Subir** el archivo (foto o PDF).'],
           marks=[g.field('document_type'), g.field('avatar')],
           crop='top')
    g.page.locator('.o_list_button_save:visible').first.click()
    g.wait(1200)
    g.step('Pulsa **Guardar**. Repite con el DNI (tipo *Tarjeta de identificación con foto*). Vuelve al contrato con la miga de pan de arriba.',
           marks=[row, g.page.locator('.o_breadcrumb a').first], crop='top',
           tip='Para ver un documento guardado, pulsa en su nombre de archivo y se descarga.')
