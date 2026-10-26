TASK = dict(
    id='devolver-fianza-despues',
    title='Devolver la fianza más tarde (botón «Devolver fianza»)',
    short='Fianza más tarde',
    cat='cobros',
    summary='Si en la devolución no marcaste devolver la fianza (por ejemplo, esperabas el presupuesto de un daño), puedes devolverla después desde el contrato.',
    when='El contrato ya está Devuelto y la fianza sigue sin devolver.',
    before=['El contrato está **Devuelto** (o Cancelado) y tiene fianza cobrada.'],
    tags=['fianza', 'deposito', 'devolver fianza', 'pendiente', 'tarde', 'despues'],
    result='Se crea la rectificativa de la fianza. Confírmala y registra el pago como en [[devolver-fianza]].',
    next=['devolver-fianza'],
)


def run(g):
    cid = g.new_contract('0999-DMO', 'Cliente Demo SL', start_in=-4, days=3, driver='Pepe Demo García')
    g.quick_return(cid, km=310, refund=False)
    g.open_contract(cid)
    g.step('En el contrato **Devuelto**, pulsa **Devolver fianza**.', marks=[g.page.locator('button', has_text='Devolver fianza').first], crop='top',
           detail='El botón solo sale si hay fianza cobrada y todavía **no** se ha devuelto.')
    g.page.locator('button', has_text='Devolver fianza').first.click()
    g.wait(1500)
    modal = g.page.locator('.modal-content').last
    g.fill('return_deposit', '300')
    g.step('Pon **cuánto se devuelve** y pulsa **Crear factura**.',
           labels=['**Fianza total**: la fianza cobrada.', '**Importe a devolver**: lo que le devuelves (si se queda una parte por daños, pon solo el resto).', 'Pulsa **Crear factura**.'],
           marks=[[g.label('total_deposit'), g.field('total_deposit')], [g.label('return_deposit'), g.field('return_deposit')],
                  modal.locator('button[name=create_return_deposit_invoice]')],
           crop=modal,
           warn='No puedes devolver **más** de lo que se cobró.')
    modal.locator('button[name=create_return_deposit_invoice]').click()
    g.wait(2000)
    g.step('Se abre la rectificativa en **Borrador**. Pulsa **Confirmar** y luego **Registrar pago**, igual que en [[devolver-fianza]].',
           marks=[g.button(name='action_post')], crop='top')
