

function handle_network_errors (response) {
     if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}


function create_job(e) {
    e.preventDefault();
    const url = e.currentTarget.action;
    const data = Object.fromEntries(new FormData(e.target))
    const csrftoken = getCookie('csrftoken');
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    }).then(function (response) {
		if (response.ok) {
			return response.json();
		}
		return Promise.reject(response);
	}).then(function (data) {
		console.log(data);
	}).catch(function (error) {
		console.warn(error);
	});
}

function control_job(action, id) {
        console.log(`control_job ${id} ${action}`);
        const data = {
            action: action,
            id: id
        };
        let msg = `Do you really want to ${action} the job?`;

        if (action === "delete") {
            msg = "Do you really want to delete the job? This also deletes the Job history!"
        }
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
            .then(response => response.text())
            .then(text => console.log(text))
            .catch(error => console.log(error));

}
