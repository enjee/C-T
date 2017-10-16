var websocket = null;
var connected = false;

new function () {

    var serverUrl = "ws://localhost:8989";
    var connectionStatus;
    var sendMessage;

    $(function () {
        close();
        open();
    });

    var open = function () {
        websocket = new WebSocket(serverUrl);
        websocket.onopen = onOpen;
        websocket.onclose = onClose;
        websocket.onmessage = onMessage;
        websocket.onerror = onError;
    }

    var close = function () {
        if (websocket) {
            websocket.close();
        }
        connected = false;
    }
    var onOpen = function () {
        connected = true;
    };

    var onClose = function () {
        websocket = null;
    };

    var onMessage = function (event) {
        parseData(event.data);
    };

    var onError = function (event) {
        showErrorPopup("Connection to the websocket could not be initialized.");
    }
}