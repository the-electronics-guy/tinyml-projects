function sendCommand(command) {
    fetch('/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command: command }),
    })
    .then(response => response.json())
    .then(data => console.log('Success:', data))
    .catch((error) => console.error('Error:', error));
}

function connectToRover() {
    const ipAddress = document.getElementById('ipAddress').value;
    if (ipAddress) {
        // Handle IP connection logic here
        console.log("Connecting to Rover at IP: " + ipAddress);
    }
}
