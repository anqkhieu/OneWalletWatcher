require('dotenv').config({ path: '../.env' })
const StreamrClient = require('streamr-client')
const axios = require('axios')
var fs = require('fs')

const client = new StreamrClient({
    auth: {
        privateKey: process.env['STREAMR_PRIVATE_KEY'],
    }
})

async function getSessionToken() {
  const bearerToken = await client.session.getSessionToken()
	return bearerToken
}

getSessionToken().then(bearerToken => {
	console.log(bearerToken)

	const url = `https://streamr.network/api/v1/streams/${process.env['STREAMR_ID_URI']}/data/partitions/0/last`
	// const url = `https://streamr.network/api/v1/streams/${process.env['STREAMR_ID_URI']}/data/partitions/0/range`

	axios.get(url, {
	    headers: {
				"Content-Type": "application/json",
		    "Authorization": `Bearer ${bearerToken}`
	    },
			params:{
				"count": fs.readFileSync('../node/config.txt', 'utf8')
		  }
	  })
	  .then(function (response) {
			console.log(response['data'])
			fs.writeFile("../DiscordBot/stream.json", JSON.stringify(response['data']), (err) => {
			  if (err)
			    console.log(err)
			  else {
			    console.log("File written successfully\n")
			    console.log("The written has the following contents:")
			    console.log(fs.readFileSync("../DiscordBot/stream.json", "utf8"))
			  }
			})
	  })
	  .catch(function (error) {
	    console.log(error)
	  })
	  .then(function () {
	    // tbd
	  })

}).catch(err => {
	console.log(err)
})
