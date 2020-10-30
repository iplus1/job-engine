
function job_table() {
    return new Tabulator('#jobtable', {
        layout: 'fitDataStretch',
        placeholder: 'No Data Received',
        ajaxURL: 'get_jobs/',
        ajaxLoader: false,
        pagination: 'local',
        paginationSize: 6,
        columns: [
            {title: 'Name', field: 'name', width: 128},
            {title: 'Mode', field: 'mode', width: 128},
            {title: 'Crontab', field: 'cron_string', widthGrow: 1},
            {title: 'Optional Parameters', field: 'optional_params', width:256},
            {title: 'Running', field: 'running', widthGrow: 1},
            {title: 'Status', field: 'status', widthGrow: 1},
            {title: 'Date', field: 'date', widthGrow: 2},
            {title: 'Control Panel', field: 'control', width: 64, formatter: (cell) => {
                return generate_control(cell.getRow().getData())
                }},
            ]
    })
}
