TASK = dict(
    id='imprimir-enviar',
    title='Imprimir o enviar el contrato al cliente',
    short='Imprimir / enviar',
    cat='entrega',
    summary='Saca el contrato en PDF para firmarlo en papel, o mándaselo al cliente por correo.',
    when='Antes de entregar la furgoneta, para que el cliente lo lea y lo firme.',
    before=['El contrato está revisado y guardado ([[revisar-contrato]]).',
            'El cliente tiene **correo electrónico** en su ficha (para enviarlo).'],
    tags=['pdf', 'imprimir', 'papel', 'enviar correo', 'mandar contrato', 'firma', 'firmar'],
    result='El cliente tiene su contrato: en papel firmado, o en su correo. El envío queda apuntado en el historial de la derecha.',
    next=['entregar'],
)


def run(g):
    g.open_contract(g.find('vehicle.contract', [['vehicle_id.license_plate', '=', '0777-DMO']])['id'])
    g.step('En el contrato, arriba tienes los dos botones:',
           labels=['**Imprimir Contrato**: descarga el PDF para imprimirlo.',
                   '**Enviar Contrato**: lo manda por correo al cliente con el PDF adjunto.'],
           marks=[g.button(name='action_print_contract'), g.button(name='action_send_contract_email')], crop='top')
    g.pdf('vehicle.contract', 'action_print_contract',
          'Al pulsar **Imprimir Contrato** se descarga el PDF. Así se ve: datos del cliente, furgoneta, fechas, precio y condiciones.',
          pages=(1, 2), tip='Imprímelo, que el cliente lo **firme** y guárdalo. Si lo escaneas, súbelo al botón **Documentos** del contrato.')
    g.button(name='action_send_contract_email').click()
    g.wait(2000)
    modal = g.page.locator('.modal-content').last
    g.step('Si pulsas **Enviar Contrato**, se abre el correo ya escrito con el PDF adjunto. Revisa y pulsa **Enviar**.',
           labels=['**A**: el cliente. Puedes añadir más personas.', 'El PDF del contrato va adjunto.', 'Pulsa **Enviar**.'],
           marks=[modal.locator('.o_field_widget[name=partner_ids]'), modal.locator('.o_field_widget[name=attachment_ids], .o_attachment').first,
                  modal.locator('button', has_text='Enviar').first],
           crop=modal,
           warn='Si el cliente **no tiene correo** en su ficha, el correo no le llegará. Añádelo en [[nuevo-cliente|su ficha]].')
    modal.locator('button', has_text='Descartar').first.click()
    g.wait(800)
