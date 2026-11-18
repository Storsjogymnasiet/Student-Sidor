const ESP_ADDRESS = "http://192.168.47.179/sensors";

const luxTag = document.getElementById("lux");
const temperatureTag = document.getElementById("temperature");
const aqiTag = document.getElementById("aqi");
const tvocTag = document.getElementById("tvoc");
const co2Tag = document.getElementById("co2");
const doorTag = document.getElementById("door");


async function getData() {
    Toastify({
        text: "Loading",
        duration: 3000,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: "#1B1A55",
        },
        onClick: function () { } // Callback after click
    }).showToast();
    const response = await fetch(ESP_ADDRESS);

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    Toastify({
        text: "Loading Complete!",
        duration: 3000,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: "#1B1A55",
        },
        onClick: function () { } // Callback after click
    }).showToast();

    console.log(data)
    handleData(data)
}

function handleData(data) {
    luxTag.innerHTML = data.lux.toFixed(1);
    temperatureTag.innerHTML = data.temperature.toFixed(1) + " °C";
    aqiTag.innerHTML = data.aqi
    tvocTag.innerHTML = data.tvoc
    co2Tag.innerHTML = data.eco2
    setDoorText(data.door_open)
}

function setDoorText(status) {
    doorTag.innerHTML = status ? "Open" : "Closed";
}

document.getElementById('reloadButton').addEventListener('click', async () => { getData(); });