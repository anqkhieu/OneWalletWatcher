const StreamrClient = require('streamr-client')
var fs = require('fs')

const throwaway = StreamrClient.generateEthereumAccount()


fs.writeFile("../throwaway.json", JSON.stringify(throwaway), (err) => {
  if (err)
    console.log(err)
  else {
    console.log("File written successfully\n")
    console.log("The written has the following contents:")
    console.log(fs.readFileSync("../throwaway.json", "utf8"))
  }
})
