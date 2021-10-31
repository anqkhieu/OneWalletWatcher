require('dotenv').config({ path: '../.env' })
const StreamrClient = require('streamr-client')
var fs = require('fs')

const client = new StreamrClient({
    auth: {
        privateKey: process.env.STREAMR_PRIVATE_KEY,
    }
})

const publishDataToStream = async data => {
    return new Promise( (resolve, reject) => {
        if (!process.env['STREAMR_PRIVATE_KEY']) {
            reject(new Error('Streamr Private Key is required'))
        }

        if (!process.env['STREAMR_ID']) {
            reject(new Error('Streamr Stream ID is required'))
        }

        client.publish(process.env['STREAMR_ID'], data)
            .then(() => resolve(data))
            .catch(error => reject(error))
    })
}

try {
    var data = fs.readFileSync('data.json', 'utf8');
    console.log(data.toString());
} catch(e) {
    console.log('Error:', e.stack);
}

console.log('app.js - attempting to publish data to stream')
publishDataToStream(data)
