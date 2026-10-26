TASK = dict(
    id='devolver',
    title='Recoger la furgoneta (devolución)',
    short='Devolución',
    cat='devolucion',
    summary='Cuando el cliente trae la furgoneta: apuntas km y combustible, revisas golpes, decides la fianza y el cliente firma. Todo en una sola ventana.',
    when='El cliente llega a la oficina a devolver la furgoneta.',
    before=['El contrato está **En curso** y tiene sus cuotas creadas ([[cobrar-cuotas]]).',
            'Has mirado el **cuentakilómetros** y el **nivel de combustible**.',
            'Has dado una vuelta a la furgoneta **con el cliente delante** buscando golpes y rayones.'],
    tags=['devolucion', 'recoger', 'traer furgoneta', 'devuelto', 'cerrar contrato', 'kilometros', 'combustible', 'acta', 'llaves'],
    result='El contrato pasa a **Devuelto**, la furgoneta vuelve a estar **libre** y se genera el **acta de devolución** (PDF) que le llega al cliente por correo.',
    next=['danos-devolucion', 'devolver-fianza'],
)


def run(g):
    cid = g.find('vehicle.contract', [['vehicle_id.license_plate', '=', '0777-DMO']])['id']
    g.open_contract(cid)
    g.step('Abre el contrato y pulsa **Devuelto**.', marks=[g.button(name='b_in_progress_to_c_return')], crop='top',
           detail='¿No ves el botón **Devuelto**? El contrato tiene que estar **En curso** y tener cuotas. Mira [[cobrar-cuotas]].')
    g.button(name='b_in_progress_to_c_return').click()
    g.wait(2000)
    modal = g.page.locator('.modal-content').last
    g.fill('odometer', '20120')
    g.select('fuel_level', '3/4')
    g.step('Se abre la ventana **Devolución de Vehículo**. Apunta cómo vuelve:',
           labels=['**Fecha de devolución**: ahora (cámbiala si la trajo antes).',
                   '**Kilometraje** que marca ahora. Los **km recorridos** se calculan solos.',
                   '**Combustible** con el que vuelve. Arriba ves con cuál salió.'],
           marks=[[g.label('return_date'), g.field('return_date')],
                  [g.label('odometer'), g.field('odometer'), g.field('km_driven')],
                  [g.label('fuel_level'), g.field('fuel_level'), g.field('fuel_level_start')]],
           crop=modal,
           warn='Los km de devolución **no pueden ser menos** que los de salida. Si te sale ese error, vuelve a mirar el cuentakilómetros.')
    g.check('inspection_done')
    g.step('**Inspección**: marca que has revisado la furgoneta. Si **no hay daños**, deja sin marcar «El vehículo presenta daños».',
           marks=[[g.label('inspection_done'), g.field('inspection_done')], [g.label('has_damage'), g.field('has_damage')]],
           crop=g.band(g.label('inspection_done'), g.field('has_damage')),
           stop='Sin marcar **He inspeccionado el vehículo** no se puede cerrar la devolución. Revísala **siempre** delante del cliente.',
           tip='¿Tiene un golpe o rayón nuevo? Sigue la tarea [[danos-devolucion]].')
    g.step('**Fianza**: ya viene marcado devolverla entera.',
           labels=['**Fianza cobrada** al principio.', '**Devolver la fianza**: déjalo marcado.', '**Fianza a devolver**: cámbialo si se queda una parte.',
                   '**Neto a devolver** al cliente.'],
           marks=[g.field('deposit_charged'), g.field('refund_deposit'), g.field('deposit_to_refund'), g.field('deposit_net_to_customer')],
           crop=g.band(g.sep('Fianza'), g.field('deposit_to_refund')),
           detail='Se crea la **factura rectificativa** de la fianza en borrador. Después hay que confirmarla y pagarla al cliente: ver [[devolver-fianza]].')
    g.check('request_signature')
    g.step('**Firma**: marca **Solicitar firma del cliente** y pulsa en el recuadro **FIRMA**.',
           marks=[[g.label('request_signature'), g.field('request_signature')], g.field('customer_signature')],
           crop=g.band(g.sep('Firma'), g.field('company_signature')))
    g.sign('customer_signature', 'El cliente firma en la pantalla (con el dedo en tablet, o con el ratón) y pulsa **Adoptar y firmar**.')
    g.sign('company_signature')
    g.step('Firma tú también en **Firma de la Empresa**. Abajo, deja marcado **Enviar email de cierre** para que le llegue el acta.',
           marks=[[g.field('customer_signature'), g.field('company_signature')], [g.label('send_closing_email'), g.field('send_closing_email')]],
           crop=g.band(g.sep('Firma del Cliente'), g.field('customer_email')))
    g.step('Pulsa **Confirmar Devolución**.', marks=[modal.locator('button[name=action_confirm_return]')], crop=modal.locator('.modal-footer'))
    modal.locator('button[name=action_confirm_return]').click()
    g.wait(2500)
    if g.page.locator('.modal-content').count():
        g.step('E-AFTER', crop=g.page.locator('.modal-content').last)
    g.step('El contrato queda **Devuelto**. Arriba tienes el botón de la devolución (con el acta) y **Devolver fianza** si queda pendiente.',
           marks=[g.page.locator('.o_statusbar_status'), g.page.locator('button[name=action_view_returns]')], crop='top')
