const axios = require('axios');

const url = "http://192.168.137.193:8080/test2"
// const url = "https://51967l20e0.yicp.fun/test2"

const argv = process.argv;

axios.post(url, {
    command: argv[2],
}).then((res) => {
    console.log(res.data);
}).catch((err) => {
    console.log(err);
})