// File: test.js

// Function to load a script dynamically
function loadScript(url, callback) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    script.onload = callback;
    document.head.appendChild(script);
}

// Load NeoVis.js script dynamically
loadScript('https://unpkg.com/neovis.js@2.0.2', function () {
    // NeoVis.js is loaded, now you can use it

    // Import the drawNeoVis function from hello.js
    const { drawNeoVis } = require('./hello.js');

    // Call the drawNeoVis function
    drawNeoVis();
});
