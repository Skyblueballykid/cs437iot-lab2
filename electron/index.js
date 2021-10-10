document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.1.23";   // the IP address of your Raspberry PI

function client(){
    
    const net = require('net');
    var input = document.getElementById("message").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("bluetooth").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}


// Capture the keystroke and send it to the Pi API
function sendKeystroke(e) {
    console.log(e)
    fetch(`http://${server_addr}:8080/${e}`)
    .then(res => res.json())
    .then((data) => {
        console.log(data)
        document.getElementById('temperature').innerHTML = `${data} &deg;C`
    })
    .catch((err) => {
        console.log(err)
        document.getElementById('temperature').innerHTML = 0
    })
  }

// Send a post request with the message to the Pi
function sendMessage(msg) {
    msg = document.getElementById("message").value;
    console.log(msg)
    fetch(`http://${server_addr}:8080/`, {
        method: "post",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
          //make sure to serialize your JSON body
        body: JSON.stringify({
            msg: msg
        })
        })
        .then( (response) => { 
        return response
        })   
    }


// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("68");
    }
    else if (e.keyCode == '88') {
        // stop (x)
        document.getElementById("stopCircle").style.color = "green";
        send_data("68");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
    document.getElementById("stopCircle").style.color = "grey";
}


// update data for every 50ms
function update_data(){
    setInterval(function(){
        // get image from python server
        client();
    }, 50);
}
