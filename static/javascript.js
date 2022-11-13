//Ignore everything here:)
//Bad and lazy code

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const canvasOffsetX = canvas.offsetLeft;
const canvasOffsetY = canvas.offsetTop;

let isPainting = false;
let lineWidth = 5;
let startX;
let startY;

ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

const draw = (e) => {
    if (!isPainting) {
        return;
    }

    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';

    ctx.lineTo(e.clientX - canvasOffsetX, e.clientY);
    ctx.stroke();
}

canvas.addEventListener('mousedown', (e) => {
    isPainting = true;
    startX = e.clientX;
    startY = e.clientY;
});

canvas.addEventListener('mouseup', e => {
    isPainting = false;
    ctx.stroke();
    ctx.beginPath();
});

canvas.addEventListener('mousemove', draw);

let btnPred = document.getElementById("btnPred");
let btnClear = document.getElementById("btnClear");
let out = document.getElementById("out");

btnClear.onclick = () => {
    console.log("plzwork");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
}


btnPred = document.getElementById("btnPred");
out = document.getElementById("out");

btnPred.onclick = () => {
    let img = canvas.toDataURL("img/png");
    img = img.split(",")[1]; // Removes data:image/png;base64,
    console.log("plzwork");

    /* Sends a post request to the url
       Really import that the Content-Type is set to application/json, if this is not done flask will
       fail when you try to do request.json[]
       Here the base64 of the canvas is sent under the key b64img in the request

       then the function asynchronously waits for the response given from the server
       which is printed to the out variable
     */

       //When running on non local server change this to what app.py runs on
    fetch("http://localhost:5000/predictImage", { 
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"b64img": img}),
    }).then(async response => {
        if (response.ok) {
            out.innerText += await response.text();
            return
        }
        throw new Error('Request failed!');
    }, networkError => {
        console.log(networkError.message);
    })
}
