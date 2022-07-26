/** @odoo-module **/

import { _t } from 'web.core';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const loginWithMetamaskService = {
    dependencies: [],
    start(env, {}) {
        console.log(env);
        console.log(document);
        var eth_chainId = "0x1";
        var address_element = document.getElementById("metamask-address");
        
        document.addEventListener("DOMContentLoaded", function(event) {
            console.log("DOMContentLoaded");
        });

        window.onload = function() {
            console.log("WINDOW ONLOAD");
        };

        var metamask_login = document.getElementById("metamask-login");
        if (!metamask_login) {
            return;
        }

        if (!window.ethereum) {
            metamask_login.disabled = true;
            return;
        }
        
        if (window.ethereum.chainId) {
            if (window.ethereum.chainId != eth_chainId) {
                metamask_login.disabled = true;
                address_element.innerText = "Please select Ethereum Mainnet";
                return;
            }
        }

        metamask_login.disabled = false;
        if (window.ethereum.selectedAddress) {
            address_element.innerText = window.ethereum.selectedAddress;
        }

        var call_ajax = function callAjax(url, data, callback) {
            var xmlhttp;
            xmlhttp = new XMLHttpRequest();
            xmlhttp.onreadystatechange = function() {
                console.log("onreadystatechange", xmlhttp);
                if (xmlhttp.readyState == 4) {
                    callback(xmlhttp);
                }
            };
            xmlhttp.open("POST", url, true);
            //data.csrf_token = odoo.csrf_token;
            //xmlhttp.setRequestHeader("Content-Type", "application/json");            
            xmlhttp.send(data);
        };

        window._web3 = new Web3(window.ethereum);
        
        metamask_login.addEventListener("click", function(event) {

            window.ethereum.request({
                method: "eth_requestAccounts"
            }).then((accounts) => {
                if (window.ethereum.chainId != eth_chainId) {
                    alert("Please select Ethereum Mainnet");
                    return;
                } else {
                    console.log(accounts);
                    var sign_string = function(string) {
                        window._web3.eth.personal.sign(window._web3.utils.utf8ToHex(string),
                                                       accounts[0],
                                                       "nft_sniper")
                            .then(function(res) {
                                var formData = new FormData();
                                formData.append("address", accounts[0]);
                                formData.append("chain_id", window.ethereum.chainId);
                                formData.append("signature", res);
                                formData.append("csrf_token", window.odoo.csrf_token);
                                
                                call_ajax("/nft_sniper/login_with_metamask", formData, function(xhr) {
                                    console.log("XHR", xhr);
                                    if (xhr.status == 200) {
                                        window.location.href=xhr.responseURL;
                                    }
                                });                                
                            });
                    };                    
                    sign_string(accounts[0]);
                }
            });
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

