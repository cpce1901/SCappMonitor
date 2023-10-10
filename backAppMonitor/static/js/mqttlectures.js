const Mqtt = (data) => {
    const { server, port, user, pass, base, ubicacion, sensor } = data[0];
    
    var clientId = "ws" + Math.random();
    var username = user;
    var password = pass;

    const direction = base + "/" + ubicacion + "/" + sensor;
    console.log(direction)
    // Create a client instance
    var client = new Paho.MQTT.Client(server, port, clientId);

    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // connect the client
    client.connect({
        onSuccess: onConnect,
        userName: username,
        password: password,
    });

    // called when the client connects
    function onConnect() {
        // Once a connection has been made, make a subscription and send a message.
        console.log("Conectado MQTT-WebSocket");
        client.subscribe(direction);
    }

    // called when the client loses its connection
    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("Conexión perdida:" + responseObject.errorMessage);
        }
    }

    // called when a message arrives
    function onMessageArrived(message) {
        console.log(message.destinationName + ": " + message.payloadString);

        if (message.destinationName == direction) {
            try {
              var data_entry = JSON.parse(message.payloadString);
      
              var allValuesValid = true;
      
              for (var i in data_entry) {
                if (data_entry[i] === "" || data_entry[i] === null) {
                  allValuesValid = false;
                  break;
                }
              }
      
              if (allValuesValid) {
                for (var i in data_entry) {
                  if (i.includes("sensor"))
                    document.getElementById(i).textContent = data_entry[i];
                  if (i.includes("v"))
                    document.getElementById(i).textContent =
                      data_entry[i] + " " + "V";
                  if (i.includes("i"))
                    document.getElementById(i).textContent =
                      data_entry[i] + " " + "A";
                  if (i.includes("p"))
                    document.getElementById(i).textContent =
                      data_entry[i] + " " + "Kw";
                  if (i.includes("pa"))
                    document.getElementById(i).textContent =
                      data_entry[i] + " " + "Kw/h";
                  if (i.includes("fp"))
                    document.getElementById(i).textContent = data_entry[i];
                  if (i.includes("hz"))
                    document.getElementById(i).textContent =
                      data_entry[i] + " " + "Hz";
                }
              }
            } catch (error) {
              console.log(error);
            }
          }

    }
};

window.onload = function () {
    try {
        var data = JSON.parse(
            document.getElementById("json_data").getAttribute("data-json")
        );

        Mqtt(data);

    } catch (error) {
        console.log(error);
    }
};
