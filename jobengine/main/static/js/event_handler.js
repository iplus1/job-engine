
function ready(callbackfunc) {
    if (document.readyState !== 'loading') {
        callbackfunc();
    } else if (document.addEventListener) {
        document.addEventListener('DOMContentLoaded', callbackfunc);

    } else {
        document.attachEvent ('onreadystatechange', function() {
            if (document.readyState === 'complete') {
                callbackfunc();
            }
         });
    }
}


ready(function () {
    document.querySelector("#jobform").addEventListener('submit', function (e) {
        console.log('Submit Create');
        create_job(e);
    });

    document.querySelector('#mode').addEventListener("change",function(e) {
        const cron_string = document.querySelector('#cronstring');
        if (this.value === "cmd") {
            hide_element(cron_string);
        }
        else {
            show_element(cron_string);
        }
  });
    let table = job_table()
    update_table(table)
});

