/** @odoo-module **/

import AbstractFieldOwl from 'web.AbstractFieldOwl';
import FieldRegistry from 'web.field_registry_owl';

const {useState} = owl.hooks;

export class WarningWidget extends AbstractFieldOwl {
    constructor(...args) {
        super(...args);
    }

    setup() {
        if (!('empty_val' in this.attrs)) {
            throw new Error('You must specify empty_val to use widget="zwarning"')
        }
        this.state = useState({
            isEmpty: !(this.val === this.attrs['empty_val']),
            tooltip: this.attrs['empty_tooltip'] ?? ''
        })
    }
}

WarningWidget.template = owl.tags.xml`
<div data-toggle="tooltip" data-placement="top" t-attf-title="{{ state.tooltip }}">
    <span t-esc="_formatValue(value)"/>
    <i t-if="state.isEmpty" class="fa fa-exclamation-triangle ml-2 text-danger"/>
</div>
`
AbstractFieldOwl.supportedFieldTypes = ['float'];

FieldRegistry.add('zwarning', WarningWidget);
