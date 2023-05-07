
async function read_logs(url, log_path, log_file){
    let response = await fetch(url,{
        'method': 'post',
        'body': JSON.stringify({log_path:log_path, log_file:log_file})
    })
    .then((res) => res.json())
    .then((data) => data)
    .catch((error) => console.log('fetch error:', error));
    // console.log(response);
    return response;
}

function run(){
    let file_length = 0;
    let first_line = 0;
    var continue_read = true;
    let log_path = document.getElementById("log_path_id").value
    let log_file = document.getElementById("log_file_id").value
    read_logs(window.location.href, log_path, log_file)
    .then((data) => {
        if(data != undefined){
            file_length = data['length'];
            first_line = file_length;
            // document.getElementById("log_results").innerHTML = data['length']
            document.getElementById("state_text").innerHTML = data['message'];
            //data['data'].forEach((record) => {
            //    document.getElementById("log_results").innerHTML += '<pre style="margin:0px;">' + record + '</pre>';
            //    });
            }
    });



    window.onscroll = function(ev) {
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
            continue_read = true;
        }else{
            continue_read = false;
        }
    };

    let timerId = setInterval(() => {
       if( document.getElementById('continue_read_checked').checked && continue_read){
        let div_content = document.getElementById("log_results").innerHTML;
        let div_length = div_content.split('</pre>').length;
        let first_line_end = 0
            let is_live_read = document.getElementById('is_live_read').innerHTML;
            document.getElementById('is_live_read').innerHTML = is_live_read == 'Reading' ? '' : 'Reading'
            let log_path = document.getElementById("log_path_id").value
            let log_file = document.getElementById("log_file_id").value
            read_logs(window.location.href, log_path, log_file)
            .then((data) => {
                if (data != undefined && data['length'] != file_length){
                    document.getElementById("state_text").innerHTML = data['message'];
                    document.getElementById("file_size").innerHTML = data['file_size'];
                    if (div_length > 1500){
                        for(let i=0; i<(div_length - 1500); i++){
                            first_line_end = div_content.search('</pre>');
                            div_content = div_content.slice(first_line_end + 6);
                        }
                            document.getElementById("log_results").innerHTML = div_content;
                    }
                    file_length = data['length']
                    data['data'].forEach((record) => {
                        document.getElementById("log_results").innerHTML += '<pre style="margin:0px;">' + record + '</pre>';
                    });
                }
            })
            window.scrollTo(0, document.body.scrollHeight);

        }else{
            document.getElementById('is_live_read').innerHTML = 'Stopped';
        }
    }, 800);


}

function read_data(){
            let log_path = document.getElementById("log_path_id").value
            let log_file = document.getElementById("log_file_id").value
            read_logs(window.location.href,log_path, log_file)
            .then((data) => {
            document.getElementById("state_text").innerHTML = data['message'];
                   file_length = data['length']
                    data['data'].forEach((record) => {
                        document.getElementById("log_results").innerHTML += '<pre style="margin:0px;">' + record + '</pre>';
                    });
            });
}

run();