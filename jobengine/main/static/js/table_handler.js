/**
 * Handle the onClick event of the cells in the job.table.
 *
 * Display the information of the cell in a help modal.
 *
 * @param cell: Expects a cell-object of the job-table.
 */
on_cell_click = function (cell) {
    const help_modal = document.querySelector("#help_modal");
    const title = `Job ${cell.getColumn().getDefinition().title}`;
    let body_value = cell.getValue();
    if (title.includes('Status')) {
        if (cell.getValue() === null) {
            body_value = 'Waiting on Execution...';
        } else if (cell.getValue() === 137) {
            body_value = `Return Code: ${cell.getValue()} Process has been stopped.`;
        } else {
            body_value = `Return Code: ${cell.getValue()}`;
        }
    } else if (title === 'Job Running') {
        if (cell.getValue() === true) {
            body_value = 'Yes';
        } else {
            body_value = 'No';
        }
    } else {
        if (cell.getValue() === null) {
            body_value = 'No Data Available.';
        }
    }
    let body = `<pre>${body_value}</pre>`;
    fill_help_modal(title, body);
    show_element(help_modal);
}

/**
 * Returns the Tabulator object of the job-table.
 *
 * Contains the definition for the job-table.
 *
 * @returns {Tabulator}
 */
function job_table() {
    return new Tabulator('#job_table', {
        layout: 'fitDataStretch',
        placeholder: 'No Data Received',
        ajaxURL: 'get_jobs/',
        ajaxLoader: false,
        pagination: 'local',
        paginationSize: 14,
        tooltips: true,
        columns: [
            {
                title: 'Name',
                field: 'name',
                width: 120,
                cellClick: (e, cell) => on_cell_click(cell)
            },
            {
                title: 'Mode',
                field: 'mode',
                width: 90,
                cellClick: (e, cell) => on_cell_click(cell)
            },
            {
                title: 'Crontab',
                field: 'cron_string',
                width: 90,
                cellClick: (e, cell) => on_cell_click(cell)
            },
            {
                title: 'Command / Ipynb',
                field: 'command_ipynb',
                width: 300,
                cellClick: (e, cell) => on_cell_click(cell)
            },
            {
                title: 'Running',
                field: 'running',
                width: 100,
                cellClick: (e, cell) => on_cell_click(cell),
                formatter: (cell) => {
                    if (cell.getValue() === true) {
                        return `Yes`;
                    } else {
                        return `No`;
                    }
                }
            },
            {
                title: 'Status',
                field: 'current_status',
                hozAlign: "center",
                width: 105,
                cellClick: (e, cell) => on_cell_click(cell),
                titleFormatter: (element) => {
                    return `${element.getValue()}  <a href="#" onclick="get_help('status_help_holder')">
                            <span class="glyphicon glyphicon-question-sign"></span></a></label>`;
                },
                formatter: (cell) => {
                    return status_button(cell.getValue());
                },
                tooltip: function (cell) {
                    if (cell.getValue() === null) {
                        return 'Waiting on Execution...';
                    } else if (cell.getValue() === 137) {
                        return 'Return Code: 137 Process has been stopped.';
                    } else {
                        return `Return Code: ${cell.getValue()}`;
                    }
                }
            },
            {
                title: 'Output',
                field: 'output',
                width: 200,
                cellClick: (e, cell) => on_cell_click(cell)
            },
            {
                title: 'Start Date',
                field: 'start_date',
                width: 160,
                cellClick: (e, cell) => on_cell_click(cell)
            },
            {
                title: 'End Date',
                field: 'end_date',
                width: 160,
                cellClick: (e, cell) => on_cell_click(cell)
            },
            {
                title: 'Control Panel',
                field: 'control',
                titleFormatter: (element) => {
                    return `${element.getValue()}  <a href="#" onclick="get_help('control_help_holder')">
                            <span class="glyphicon glyphicon-question-sign"></span></a></label>`;
                },
                formatter: (cell) => {
                    return generate_control(cell.getRow().getData());
                }
            },
        ]
    });
}

