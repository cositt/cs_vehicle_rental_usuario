TASK = dict(
    id='conductor-empresa',
    title='Añadir un conductor a una empresa',
    short='Conductor de empresa',
    cat='clientes',
    summary='Cuando el cliente es una empresa, la furgoneta la conduce un empleado suyo. Se añade como contacto de la empresa con sus datos de carnet, y luego se elige en el contrato.',
    when='Una empresa alquila y te dice quién va a conducir.',
    before=['La empresa ya está dada de alta ([[nuevo-cliente]]).', 'Tienes el carnet del conductor.'],
    tags=['conductor', 'chofer', 'empleado', 'empresa', 'contacto', 'carnet', 'conductor autorizado'],
    result='El conductor aparece en el campo **Conductor** del contrato de esa empresa, y al elegirlo el contrato copia solo su carnet.',
    next=['revisar-contrato'],
)


def run(g):
    p = g.find('res.partner', [['name', '=', 'Cliente Demo SL']])
    g.url(f"/odoo/res.partner/{p['id']}")
    g.page.wait_for_selector('.o_form_view', timeout=30000)
    g.wait(800)
    tab = g.tab('Contactos')
    tab.click()
    g.wait(600)
    children = g.page.locator('.o_field_widget[name=child_ids]')
    add = children.get_by_text('Añadir Contacto').first
    g.step('Abre la ficha de la **empresa**, ve a la pestaña **Contactos** y pulsa **Añadir Contacto**.',
           marks=[tab, add], crop=g.band(tab, children))
    add.click()
    g.wait(1500)
    modal = g.page.locator('.modal-content').last
    g.fill('name', 'Luis Conductor Demo')
    g.fill('phone', '600 000 005')
    g.step('Escribe el **nombre** del conductor y su teléfono.', marks=[g.field('name'), g.field('phone')], crop=modal,
           detail='El tipo de contacto déjalo en **Contacto**.')
    modal.locator('.modal-footer button', has_text='Guardar y cerrar').first.click()
    g.wait(1200)
    g.save()
    luis = children.locator('.o_kanban_record', has_text='Luis Conductor Demo').first
    g.step('Guarda la empresa. Luis ya sale entre sus contactos.',
           marks=[luis], crop=g.band(g.tab('Contactos'), children))
    luis_id = g.find('res.partner', [['name', '=', 'Luis Conductor Demo']])['id']
    g.url(f"/odoo/res.partner/{luis_id}")
    g.page.wait_for_selector('.o_form_view .o_notebook', timeout=30000)
    g.wait(800)
    tab = g.tab('Conducción')
    tab.click()
    g.wait(600)
    g.fill('driver_identity_number', '33333333P')
    g.fill('birth_date', '02/06/1985')
    g.fill('driver_license_number', '33333333P')
    g.fill('driver_license_issue_date', '10/01/2012')
    g.fill('driver_license_expiry_date', '10/01/2032')
    g.step('Ahora abre la ficha de **Luis** (búscalo en **Clientes**), pestaña **Conducción**, y pon su DNI, nacimiento y **carnet**.',
           labels=['Pestaña **Conducción**.', 'DNI y fecha de nacimiento.', 'Carnet: número, expedición y caducidad.'],
           marks=[tab, [g.field('driver_identity_number'), g.field('birth_date')],
                  [g.field('driver_license_number'), g.field('driver_license_issue_date'), g.field('driver_license_expiry_date')]],
           crop=g.band(tab, g.field('driver_license_number')),
           tip='En la ventanita de «Añadir Contacto» no sale esta pestaña: por eso se hace después, desde su ficha.')
    g.save()
    g.step('Guarda. En el contrato de la empresa elige a Luis en **Conductor**: el carnet se copia solo.',
           marks=[g.page.locator('.o_breadcrumb').first], crop='top')
