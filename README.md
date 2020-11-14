# BytesBump Source Code
> BytesBump is a bump bot developed by [BytesToBits](https://bytestobits.dev/discord), celebrating the release of [BytesToBits Advertising](https://bytestobits.dev/advertising)! You can host this bot on your own, and we have linked a tutorial below on how to do it!

## Installation
- You can host the bot on [Repl.it](https://repl.it/) or [Heroku](https://heroku.com). However, we recommend getting a proper VPS for your bot.
- Download the files.
- Open `Admin/config.yml`.
- Leave the tab open head over to [Discord Applications](https://discord.com/developers/applications/).
- Create a new application. Give it a name and a profile picture.
- Once it's created, click on the `Bot` tab in the left side of your screen.
- Make the application a bot and copy its token.
- Paste the token in the **token: `token`** area.
- Feel free to change the prefix if you want to.
- Now, head over to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a new account.
- Choose the free cluster, and click `Create Cluster`,
- Head over to the `Database Access` tab below the security text.
- Add a new Database user. Give it a name and generate a new password. Make sure you save the password!
- Go to Network Access > Add IP Address > Allow access from everywhere.
- Go back to the `Clusters` tab and wait for it to be done setting up.
- Once it's done, click `CONNECT`.
- Choose `Connect your application`, and copy the URI. It must look something like this; `mongodb+srv://username:<password>@cluster4.eak2.mongodb.net/<dbname>?retryWrites=true&w=majority`, *Something like this!*
- Copy that, remove the `/<dbname>?retryWrites=true&w=majority` part, and replace `<password>` with the user password.
- Paste the URI in the `mongo` section of `config.yml`.
- Run the bot and you're done! You are free to modify everything you want to so it fits your server.
- Need extra help? Visit our [Discord Server](https://bytestobits.dev/discord)!