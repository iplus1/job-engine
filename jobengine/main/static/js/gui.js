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
 * Only show the cleanup, update and logs button for ipynb-jobs.
 *
 * @param data: Expects an object containing the data of a cell in the job-table.
 * @returns {string}: Contains all necessary buttons for a cell in the job-table.
 */
function generate_control(data) {
    let control_action = '';
    let control_action_color = '';
    if (data['running'] === true) {
        control_action = 'Stop';
        control_action_color = 'btn-warning';
    } else {
        control_action = 'Start';
        control_action_color = 'btn-success';
    }

    let cleanup_btn = ``;
    let update_btn = ``;
    let logs = ``;
    let start_stop_btn = ``;

    if (data['mode'] === 'cmd' || data['mode'] === 'ipynb' || (data['mode'].includes('cron') && data['running'] === true)) {
        start_stop_btn = `<input type="button"  class="btn ${control_action_color} btn-xs" value="${control_action}" onclick="trigger_action('${control_action.toLowerCase()}','${data['id']}', '${data['name']}')"/>`;
    }

    if (data['mode'].includes('ipynb')) {
        cleanup_btn = `<input type="button" class="btn btn-info btn-xs" value="Cleanup" onclick="trigger_action('cleanup','${data['id']}', '${data['name']}')"/>`;
        update_btn = `<input type="button" class="btn btn-info btn-xs" value="Update" onclick="trigger_action('update','${data['id']}', '${data['name']}')"/>`;
        logs = `<input type="button" class="btn btn-info btn-xs" value="Logs" onclick="trigger_action('logs','${data['id']}', '${data['name']}')"/>`;
    }
    const delete_btn = `<input type="button" class="btn btn-danger btn-xs" value="Delete" onclick="trigger_action('delete','${data['id']}', '${data['name']}')"/>`;
    return `<span>${start_stop_btn} ${cleanup_btn} ${update_btn} ${logs} ${delete_btn}</span>`;
}

