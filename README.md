# One Wallet Watcher

Make portfolio analysis and asset valuations fast, free, and easy! Create new wallets, get your portfolio performance minute-to-minute, distill relevant investment info, curate blockchain and crypto news, and more-- all with a Discord bot.

 Commented code and easily editable!
 Feel free to fork.

# Setup

1. Create a .env file, add it to .gitignore.

2. Use the following JS code to generate a private key Ethereum account.
```
const throwaway = StreamrClient.generateEthereumAccount()
console.log(throwaway.address)
console.log(throwaway.privateKey)
```

3. Copy and paste the throwaway address and private key into the .env file as `STREAMR_ADDRESS` and `STREAMR_PRIVATE_KEY`.

4. Add a STREAMR_ID to the .env file. (Eg: `{0xStreamrID}/OneWalletWwatcher`).

5. Share the Stream with that generated throwaway account's address as a publisher. Make sure the shared account is marked as an "Owner" in order to have all necessary permissions to push to and manage the data to the Streamr blockchain.

6. Add your Etherscane API key to the .env file.
![Example Sharing](https://i.gyazo.com/8e7d498f7f81c7a05e1b0959d8098d39.png)

7. Run `app.py`.

8. Go back to Streamr and check for data.
