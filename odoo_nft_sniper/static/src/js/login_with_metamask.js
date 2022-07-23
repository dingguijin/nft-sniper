/** @odoo-module **/

import { _t } from 'web.core';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const loginWithMetamaskService = {
    dependencies: [],
    start(env, {}) {
        console.log("loginWithMetamaskService");
    }
};

registry.category("services").add("loginWithMetamaskService", loginWithMetamaskService);
