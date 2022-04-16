/** @odoo-module **/

import { registry } from '@web/core/registry';

const systrayRegistry = registry.category('systray');

class FullScreenButton extends owl.Component {

    toggleFullScreen () {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
        else {
            document.querySelector('html').requestFullscreen();
        }
    }
}
FullScreenButton.template = owl.tags.xml`
<div class="dropdown">
    <a role="button" t-on-click="toggleFullScreen">
        <i class="fa fa-arrows-alt"/>
    </a>
</div>
`;

systrayRegistry.add("zflex.FullScreenButton", { Component: FullScreenButton }, {sequence: 100});