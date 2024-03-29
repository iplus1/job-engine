/**
 * Handle all gui related functions like the creation, show and hide of elements.
 */

/**
 * Show a specified element.
 *
 * @param element: Expect a valid HTML element.
 */
function show_element(element) {
    element.style.display = 'block';
}

/**
 * Hide a specified element.
 *
 * @param element: Expect a valid HTML element.
 */
function hide_element(element) {
    element.style.display = 'none';
}

/**
 * Fill the notification modal with a title and content for the body part.
 *
 * @param title: Expects a string to insert to the modal as a title.
 * @param body: Expects a string to insert to the modal in the body part.
 */
function fill_notification_modal(title, body) {
    document.querySelector('#notification_modal-title').innerHTML = title;
    document.querySelector('#notification_modal-body').innerHTML = body;
}

/**
 * Fill the help modal with a title and content for the body part.
 *
 * @param title: Expects a string to insert to the modal as a title.
 * @param body: Expects a string to insert to the modal in the body part.
 */
function fill_help_modal(title, body) {
    document.querySelector('#help_modal-title').innerHTML = title;
    document.querySelector('#help_modal-body').innerHTML = body;
}


function fill_edit_modal(id, name, mode, cron, command_ipynb) {
    document.querySelector('#edit_job_id').value = id;
    document.querySelector('#edit_job_name').value = name;
    document.querySelector('#edit_mode').value = mode;
    document.querySelector('#edit_cron_string').value = cron;
    if (mode.includes('ipynb')) {
        document.querySelector('#edit_ipynb_file').value = command_ipynb;
    } else {
        document.querySelector('#edit_command').value = command_ipynb;
    }
}

/**
 * Create an input field with the 'btn-circle'-class assigned to make it round.
 *
 * For better and direct visibility of the current status of the job.
 *
 * @param status: expects an integer or null that represents the current status of the job.
 * @returns {string}: The input element of for the Status cell.
 */
function status_button(status) {
    if (status === null) {
        return `<input type="button" class="btn btn btn-circle btn-sm" style="background-color: grey"/>`;
    } else if (status > 0) {
        return `<input type="button" class="btn btn-danger btn-circle btn-sm"/>`;
    } else {
        return `<input type="button" class="btn btn-success btn-circle btn-sm"/>`;
    }
}

/**
 * Create all necessary control buttons for the Control cell of the J
 * job-table.
 *
 * Only show the start button for jobs with the 'mode' set to 'cmd'.
 * Only show the stop button for jobs that are currently running.
 * Only show the cleanup, update and html button for ipynb-jobs.
 *
 * @param data: Expects an object containing the data of a cell in the job-table.
 * @returns {string}: Contains all necessary buttons for a cell in the job-table.
 */

function generate_control(data) {
    let control_action = '';
    let control_action_color = '';
    let control_action_enable = '';
    let control_action_enable_color = '';
    if (data['running'] === true) {
        control_action = 'Stop';
        control_action_color = 'btn-warning';
    } else {
        control_action = 'Start';
        control_action_color = 'btn-success';
    }

    let update_btn = ``;
    let start_stop_btn = ``;
    let enable_btn = ``;
    let html_outputs = ``;
    if (data['mode'] === 'cmd' || data['mode'] === 'ipynb' || (data['mode'].includes('cron') && data['running'] === true)) {
        start_stop_btn = `<input type="button"  class="btn ${control_action_color} btn-xs" value="${control_action}" onclick="trigger_action('${control_action.toLowerCase()}','${data['id']}')"/>`;
    }
    if (data['mode'].includes('cron')) {
        if (data['enabled'] === true) {
            control_action_enable = 'Disable';
            control_action_enable_color = 'btn-warning';
        } else {
            control_action_enable = 'Enable';
            control_action_enable_color = 'btn-success';
        }
        enable_btn = `<input type="button"  class="btn ${control_action_enable_color} btn-xs" value="${control_action_enable}" onclick="trigger_action('${control_action_enable.toLocaleLowerCase()}','${data['id']}')"/> `;
    }
    if (data['mode'].includes('ipynb')) {
        update_btn = `<input type="button" class="btn btn-info btn-xs" value="Update" onclick="trigger_action('update','${data['id']}')"/>`;
        html_outputs = `<input type="button" class="btn btn-info btn-xs" value="HTML" onclick="trigger_action('html_outputs','${data['id']}')"/>`;
    }
    const cleanup_btn = `<input type="button" class="btn btn-info btn-xs" value="Cleanup" onclick="trigger_action('cleanup','${data['id']}')"/>`;
    const delete_btn = `<input type="button" class="btn btn-danger btn-xs" value="Delete" onclick="trigger_action('delete','${data['id']}')"/>`;
    const edit_btn = `<input type="button" class="btn btn-info btn-xs" value="Edit" onclick="display_edit('${data['id']}')"/>`;
    const logs = `<input type="button" class="btn btn-info btn-xs" value="Logs" onclick="trigger_action('logs','${data['id']}')"/>`;
    return `<span>${edit_btn} ${logs} ${cleanup_btn} ${delete_btn} ${enable_btn} ${start_stop_btn} ${update_btn} ${html_outputs}</span>`;
}
