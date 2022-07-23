/** @odoo-module **/

import { _t } from 'web.core';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const loginWithMetamaskService = {
    dependencies: [],
    start(env, {}) {
        console.log(env);
        console.log(document);

        document.addEventListener("DOMContentLoaded", function(event) {
            console.log("DOMContentLoaded");
        });

        window.onload = function() {
            console.log("WINDOW ONLOAD");
        };

        var metamask_login = document.getElementById("metamask-login");
        metamask_login.addEventListener("click", function(event) {
            console.log("click");
            console.log(event);
            event.preventDefault();
        });
        
        env.bus.on("WEB_CLIENT_READY", null, async () => {
            console.log("loginWithMetamask");
            // jQuery(".metamask-login").on("click", function(event) {
            //     event.preventDefault();
            //     console.log("LOGIN BUTTON");
            // });
        });
    }
};

registry.category("services").add("loginWithMetamaskService", loginWithMetamaskService);


