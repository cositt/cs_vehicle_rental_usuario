TASK = dict(
    id='entregar',
    title='Entregar la furgoneta (pasar a «En curso»)',
    short='Entregar',
    cat='entrega',
    summary='Cuando el cliente se lleva la furgoneta, pasas el contrato a «En curso». Desde ese momento la furgoneta cuenta como alquilada.',
    when='El cliente está delante, ha firmado y se va a llevar la furgoneta.',
    before=['Contrato revisado: conductor, seguro, combustible y km ([[revisar-contrato]]).',
            'Contrato firmado ([[imprimir-enviar]]).',
            '**Fianza cobrada** con la tarjeta que pone el contrato.',
            'Has revisado la furgoneta con el cliente (golpes y rayones).'],
    tags=['dar llaves', 'salida', 'activar contrato', 'en curso', 'empezar alquiler', 'recogida'],
    stop='Pulsa **En curso** solo cuando la furgoneta **sale de verdad**. Si lo pulsas antes, el sistema la da por alquilada y empieza a contar.',
    result='El contrato está **En curso** y la furgoneta sale como ocupada en la Disponibilidad. Ahora aparecen los botones **Devuelto**, **Sustituir Vehículo** y **Crear cuota**.',
    next=['cobrar-cuotas', 'devolver', 'ampliar'],
)


def run(g):
    g.open_contract(g.find('vehicle.contract', [['vehicle_id.license_plate', '=', '0777-DMO']])['id'])
    g.step('Abre el contrato (debe poner **Borrador** arriba a la derecha) y pulsa **En curso**.',
           marks=[g.button(name='a_draft_to_b_in_progress'), g.page.locator('.o_statusbar_status')], crop='top',
           labels=['Botón **En curso**.', 'Estado actual: **Borrador**.'])
    g.button(name='a_draft_to_b_in_progress').click()
    g.wait(2000)
    modal = g.page.locator('.modal-content').last
    g.step('Se abre un **correo para el cliente** con los datos de recogida y devolución. Revísalo y pulsa **Enviar**.',
           labels=['Para quién va.', 'Texto con furgoneta, fechas y oficinas.', '**Enviar** (o **Descartar** si no quieres mandarlo).'],
           marks=[modal.locator('.o_field_widget[name=partner_ids]'), modal.locator('.o_field_widget[name=body]'),
                  [modal.locator('button', has_text='Enviar').first, modal.locator('button', has_text='Descartar').first]],
           crop=modal,
           detail='Aunque pulses **Descartar**, el contrato ya ha pasado a **En curso**. El correo es solo un aviso para el cliente.')
    modal.locator('button', has_text='Enviar').first.click()
    g.wait(2000)
    g.step('Listo: arriba pone **En curso**. Fíjate en los botones nuevos.',
           labels=['Estado **En curso**.', '**Devuelto**: lo usarás cuando traiga la furgoneta.', '**Sustituir Vehículo**: por si hay que cambiarla.'],
           marks=[g.page.locator('.o_statusbar_status'), g.button(name='b_in_progress_to_c_return'), g.button(name='action_open_substitution_wizard')],
           crop='top')
