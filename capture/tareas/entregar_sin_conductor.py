TASK = dict(
    id='entregar-sin-conductor',
    title='Aviso «Entregar sin conductor»',
    short='Sin conductor',
    cat='entrega',
    summary='Si pulsas **En curso** y el contrato no tiene **conductor autorizado**, el sistema te para y te pregunta. Puedes volver y ponerlo, o entregar igualmente.',
    when='Al pulsar **En curso** te sale la ventana «Entregar sin conductor».',
    before=['Has pulsado **En curso** en un contrato en **Borrador** ([[entregar]]).'],
    tags=['sin conductor', 'conductor autorizado', 'aviso', 'falta conductor', 'carnet', 'entregar sin conductor'],
    stop='Lo normal es **volver y poner el conductor**: sin él, el contrato no tiene carnet y si hay una multa o un accidente no sabremos quién conducía.',
    result='O el contrato ya tiene conductor y carnet, o queda **En curso** sin conductor porque así lo has decidido.',
    next=['revisar-contrato', 'conductor-empresa', 'entregar'],
)


def run(g):
    cid = g.new_contract('1443-DMO', 'Cliente Demo SL', start_in=0, days=3, deliver=False)
    g.open_contract(cid)
    g.step('En este contrato el campo **Conductor** está vacío.',
           marks=[g.field('authorized_driver_id')],
           crop=g.band(g.sep('Conductor autorizado'), g.field('driver_license_expiry_date')))
    g.step('Aun así pulsas **En curso**.', marks=[g.button(name='a_draft_to_b_in_progress')], crop='top')
    g.button(name='a_draft_to_b_in_progress').click()
    g.wait(1800)
    modal = g.page.locator('.modal-content').last
    back = modal.locator('button', has_text='Volver y añadir conductor').first
    go = modal.locator('button', has_text='Entregar sin conductor').first
    g.step('Sale este aviso. Tienes dos opciones:',
           labels=['El aviso: falta el **conductor autorizado**.',
                   '**Volver y añadir conductor**: lo recomendado. Cierras, pones el conductor y vuelves a pulsar **En curso**.',
                   '**Entregar sin conductor**: solo si el responsable lo autoriza.'],
           marks=[modal.locator('.alert').first, back, go], crop=modal)
    back.click()
    g.wait(1000)
    g.m2o('authorized_driver_id', 'Pepe Demo')
    g.wait(800)
    g.step('Pon el **conductor**. Si ya tiene el carnet en su ficha, se copia solo.',
           labels=['**Conductor**.', 'Carnet, expedición y caducidad: se rellenan solos.'],
           marks=[g.field('authorized_driver_id'),
                  [g.field('driver_license_number'), g.field('driver_license_issue_date'), g.field('driver_license_expiry_date')]],
           crop=g.band(g.sep('Conductor autorizado'), g.field('driver_license_expiry_date')),
           tip='Si el conductor no existe todavía, créalo antes: [[nuevo-cliente]] o [[conductor-empresa]].')
    g.save()
    g.step('Guarda y vuelve a pulsar **En curso**: ahora ya no sale el aviso y pasa al correo de entrega.',
           marks=[g.button(name='a_draft_to_b_in_progress')], crop='top')
