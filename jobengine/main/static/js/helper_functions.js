/**
 * Contains useful functions for different use cases.
 */

/**
 * Display the status of the performed action in a modal and update the table.
 *
 * @param text: Expects a string containing information to the performed action.
 */
function display_after_control(text) {
    Tabulator.prototype.findTable('#job_table')[0].replaceData();
    fill_help_modal('Control Information', text);
    show_element(document.querySelector('#help_modal'));
}

/**
 * Display a selection of available log-files for the job.
 *
 * @param text: Expects the selection of available logs as a string.
 * @param id: Expects an integer with the id of the job.
 * @returns {Promise<void>}
 */
async function display_after_logs(text, id) {
    const notification_modal = document.querySelector('#notification_modal');
    fill_notification_modal('Log Files', text);
    show_element(notification_modal);
    if (await confirm_notification(notification_modal)) {
        const log_file = document.querySelector('#log_file').value;
        get_log(id, log_file);
    }
}

/**
 * Display a selection of available log-files for the job.
 *
 * @param text: Expects the selection of available logs as a string.
 * @param id: Expects an integer with the id of the job.
 * @returns {Promise<void>}
 */
async function display_edit(id, job_name, job_mode, job_cron, job_command) {
    const edit_modal = document.querySelector('#edit_modal');
    fill_edit_modal(id, job_name, job_mode, job_cron, job_command);
    show_element(edit_modal);
    const edit_mode = document.querySelector('#edit_mode');
    const edit_cron_string = document.querySelector('#edit_cronstring');
    const edit_ipynb_files = document.querySelector('#edit_ipynbfiles');
    const edit_command = document.querySelector('#edit_command_div');
    if (edit_mode.value === 'cmd' || edit_mode.value === 'ipynb') {
        hide_element(edit_cron_string);
    } else {
        show_element(edit_cron_string);
    }
    if (!edit_mode.value.includes('ipynb')) {
        hide_element(edit_ipynb_files);
        show_element(edit_command);
    } else {
        show_element(edit_ipynb_files);
        hide_element(edit_command);
    }
}

/**
 * Display the error that occurred while making the request.
 *
 * @param error: Expects the error that occurred as a string.
 */
function display_after_error(error) {
    fill_help_modal('Cron Information', error);
    show_element(document.querySelector('#help_modal'));
}

/**
 * Fill the helper modal with the HTML content of the 'help'-element and show it.
 */
function get_help(helper) {
    const help_modal = document.querySelector("#help_modal");
    const help = document.getElementById(helper).innerHTML;
    fill_help_modal('Help', help);
    show_element(help_modal);
}

/**
 * Trigger a specified action for a specified job.
 *
 * Fill the notification modal with the 'job_name' and the 'action' of the clicked
 * control button and asked the user for confirmation.
 * If the action is specified for 'logs' call the control_job without confirmation.
 *
 * @param action: Expect a string that specifies the requested action.
 * @param id: Expects an integer with the id of the job.
 * @param job_name: Expects a string with the name of the job.
 * @returns {Promise<void>}
 */
async function trigger_action(action, id, job_name) {
    if (action !== 'logs') {
        const notification_modal = document.querySelector("#notification_modal");
        const body = `<br> <b>Job:</b> ${job_name} <br> <b>Action:</b> ${action}`;
        fill_notification_modal('Confirm Action', body);
        show_element(notification_modal);
        if (await confirm_notification(notification_modal)) {
            control_job(action, id);
        }
    } else {
        control_job(action, id);
    }
}

/**
 * Prepare the data of a job to be displayed in a notification modal.
 *
 * @param title: Expects a string containing the title of the modal.
 * @param data: Expects an object containing the data of the specified job.
 */
function prepare_data_for_notification(title, data) {
    let body = `<br> <b>Job:</b> ${data.job_name} <br> <b>Mode:</b> ${data.mode}`;
    switch (data.mode) {
        case 'cron':
            body = `${body} <br> <b>Cron:</b> ${data.cron_string} <br> <b>Command:</b> ${data.command}`;
            break;
        case 'cmd':
            body = `${body} <br> <b>Command:</b> ${data.command}`;
            break;
        case 'cron ipynb':
            body = `${body} <br> <b>Cron:</b> ${data.cron_string} <br> <b>Notebook:</b> ${data.ipynb_file}`;
            break;
        case 'ipynb':
            body = `${body} <br> <b>Notebook:</b> ${data.ipynb_file}`;
            break;
    }
    fill_notification_modal(title, body);
}


/**
 * Trigger the create job function.
 *
 * Ask the user to confirm his input for the creation of the job.
 * Display only the necessary information for the specified 'mode' of the job.
 *
 * @param e: Expects the initial submit event.
 * @returns {Promise<void>}
 */
async function trigger_create(e) {
    const notification_modal = document.querySelector("#notification_modal");
    e.preventDefault();
    const url = e.currentTarget.action;
    const data = Object.fromEntries(new FormData(e.target));
    prepare_data_for_notification('Confirm Create', data);
    show_element(notification_modal);
    if (await confirm_notification(notification_modal)) {
        hide_element(document.querySelector('#create_modal'));
        create_job(data, url);
    }
}

/**
 * Trigger the edit job function.
 *
 * Ask the user to confirm his input for the edit of the job.
 * Display only the necessary information for the specified 'mode' of the job.
 *
 * @param e: Expects the initial submit event.
 * @returns {Promise<void>}
 */
async function trigger_edit(e) {
    const notification_modal = document.querySelector("#notification_modal");
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    prepare_data_for_notification('Confirm Changes', data);
    show_element(notification_modal);
    if (await confirm_notification(notification_modal)) {
        hide_element(document.querySelector('#edit_modal'));
        edit_job(data);
    }
}


/**
 * Simulate the sleep behavior and returning a Promise.
 *
 * @param milliseconds: Expects an integer with the milliseconds to wait.
 * @returns {Promise<unknown>}
 */
function Sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

