
function update_table(table) {

    let page = table.getPage();
    table.setData()
        .then(() => {
        table.setPage(page)});

    setTimeout(update_table, 10000, table);
}

function generate_control(data) {
    const refreshBtn = `<input type="button" id="refreshbtn" class="btn btn-info btn-xs" value="Refresh" onclick="control_job('refresh','${data['id']}')"/>`;
    const deleteBtn = `<input type="button" id="deletebtn" class="btn btn-danger btn-xs" value="Delete" onclick="control_job('delete','${data['id']}')"/>`;
    return `<span>${refreshBtn} ${deleteBtn}</span>`
}
