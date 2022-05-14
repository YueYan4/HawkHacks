import axios from 'axios';
//Have to add in html to fix import error
//<script type="module" src="./background.js"></script>
const axios = require("axios");

var url = window.location.href;
var domain = window.location.hostname;

if (domain != "www.youtube.com") {
    console.log("Invalid URL")
}

const assembly = axios.create({
    baseURL: "https://api.assemblyai.com/v2",
    headers: {
        authorization: "a30b0d235ea04ce5946b07f391afd504",
        "content-type": "application/json",
    },
});

assembly
    .post("/transcript", {
        audio_url: url
    })
    .then((res) => console.log(res.text))
    .catch((err) => console.error(err));




