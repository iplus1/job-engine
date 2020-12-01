/**
 * Handle all request related functions.
 */

/**
 * Handles unexpected network behavior like 404, 403.
 * @param response
 * @returns {response | Error}
 */
function error_handling(response) {
    if (response.ok) {
        return response
    } else {
        throw new Error(`Unexpected network behavior with Status: ${response.status}`)
    }
}

/**
 * Make a request to create a job.
 *
 * Update the job-table immediately afterwards.
 *
 * @param data: Expects an object containing the data of the create-form.
 * @param url: Expects the url for the create request.
 */
function create_job(data, url) {
    const csrftoken = getCookie('csrftoken');
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(error_handling)
        .then(response => response.text())
        .then(function (response) {
            display_after_control(response);
        })
        .catch(function (error) {
            display_after_error(error);
        });
}

/**
 * Make a request to perform a specified action for a specified job.
 *
 * If the action was specified for 'logs' display a selection of log-files linked to the job.
 *
 * @param action: Expects a string specifying the action to be performed on the job.
 * @param id: Expects an integer with the id of the job.
 */
function control_job(action, id) {
    const data = {
        action: action,
        id: id
    };
    const csrftoken = getCookie('csrftoken');
    fetch('control_job/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(error_handling)
        .then(response => response.text())
        .then(async function (response) {
            if (action !== 'logs') {
                display_after_control(response);
            } else {
                await display_after_logs(response, id);
            }
        })
        .catch(function (error) {
            display_after_error(error);
        });
}

/**
 * Update the table-data in a set interval via the Sleep function.
 *
 */
async function update_table() {
    while (true) {
        await fetch('get_jobs/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(error_handling)
            .then(response => response.json())
            .then(function (response) {
                Tabulator.prototype.findTable('#job_table')[0].replaceData(response);
            })
            .catch(function (error) {
                display_after_error(error);
            })
            .finally(async () => {
                await Sleep(2000)
            });
    }
}

/**
 * Get a specific log file.
 *
 * @param id: Expects an integer with the id of the job.
 * @param log_file: Expects the name of the specific log file to get.
 */
function get_log(id, log_file) {
    window.open(`get_log?id=${id}&log_file=${encodeURIComponent(log_file)}`);
}
