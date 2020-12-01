/**
 * Handle every event that doesnt need to be assigned in a distinct way.
 */


/**
 * Check if the readyState of the page is loading and if not call the callback function.
 *
 * @param callbackfunc: expects the ready function as a callback.
 */
function ready(callbackfunc) {
    if (document.readyState !== 'loading') {
        callbackfunc();
    } else if (document.addEventListener) {
        document.addEventListener('DOMContentLoaded', callbackfunc);

    } else {
        document.attachEvent('onreadystatechange', function () {
            if (document.readyState === 'complete') {
                callbackfunc();
            }
        });
    }
}

/**
 * Make a custom confirm function for the notification modal to handle the user interaction.
 *
 * Return a new Promise and resolve it with the appropriate user interaction (cancel = false, confirm = true)
 *
 * @param modal: expects the notification modal as an object.
 * @returns {Promise<Boolean>}
 */
function confirm_notification(modal) {
    return new Promise((resolve) => {
        const container = modal.querySelector(".container");
        window.addEventListener('click', event => {
            switch (event.target) {
                case modal:
                    if (event.target !== modal && event.target !== container) resolve(false);
                    hide_element(modal);
                    break;
                case document.querySelector('#notification_modal-tic'):
                    resolve(false);
                    hide_element(modal);
                    break;
                case document.querySelector('#notification_modal-ok'):
                    resolve(true);
                    hide_element(modal);
                    break;
                case document.querySelector('#notification_modal-close'):
                    resolve(false);
                    hide_element(modal);
                    break;
            }
        });
    });
}

/**
 * Callback for the ready function to handle everything that needs execution after the page loaded.
 *
 * Assign EventListeners to the document and handle incoming events.
 *
 */
ready(function () {
    const help_modal = document.querySelector('#help_modal');
    const create_modal = document.querySelector('#create_modal');
    const container = help_modal.querySelector('.container');
    const add_btn = document.querySelector('#add_job-btn');
    document.querySelector("#job_form").addEventListener('submit', (e) => {
        trigger_create(e);
    });

    /**
     * EventListener for the interactions with Create-Job fields.
     */
    document.querySelector('#mode').addEventListener("change", function (e) {
        const cron_string = document.querySelector('#cronstring');
        const ipynb_files = document.querySelector('#ipynbfiles');
        const command = document.querySelector('#command_div');
        if (this.value.includes('cmd')) {
            hide_element(cron_string);
        } else {
            show_element(cron_string);
        }
        if (!this.value.includes('ipynb')) {
            hide_element(ipynb_files);
            show_element(command);
        } else {
            show_element(ipynb_files);
            hide_element(command);
        }
    });

    /**
     * EventListener for the help modal interaction buttons.
     */
    window.addEventListener('click', event => {
        switch (event.target) {
            case help_modal:
                if (event.target !== help_modal && event.target !== container) return;
                hide_element(help_modal);
                break;
            case document.querySelector('#help_modal-tic'):
                hide_element(help_modal);
                break;
            case document.querySelector('#help_modal-close'):
                hide_element(help_modal);
                break;
            case create_modal:
                if (event.target !== create_modal && event.target !== container) return;
                hide_element(create_modal);
                break;
            case document.querySelector('#create_modal-tic'):
                hide_element(create_modal);
                break;
            case document.querySelector('#create_modal-close'):
                hide_element(create_modal);
                break;
            case add_btn:
                show_element(create_modal);
        }
    });
    job_table();
    update_table();
});

