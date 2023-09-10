const { Client, Collection } = require("discord.js");
const colorama = require("./src/lib/colorama");
const { sortTime } = require("./src/lib/util");
const registerCommands = require("./src/handler/interaction");
const registerEvents = require("./src/handler/events");

require("dotenv").config(
    {
        path: "./.env"
    }
)



class SchmandiClient extends Client {
    eventsSynced = 0;


    constructor() {
        super({
            intents: [
                "Guilds",
                "GuildMembers",
                "GuildBans",
                "GuildMessages",
                "MessageContent",
                "DirectMessages",
            ]
        });
        this.commands = new Collection();
        this.commandsSynced = this.commands.size;
        this.eventsSynced = this.eventsSynced;
    }
};



if (!process.env.token) {
    console.log("Failed to get env");
    process.exit(1);
}

const client = new SchmandiClient();



client.on("ready", async () => {
    console.clear();
    if (!client?.user || !client || !client.application) {
        console.log("Something went wrong");
        process.exit(1);
    }

    const { version: discordVersion } = require("discord.js");

    console.log(`${sortTime()} [${colorama.green}INFO${colorama.reset}] [${colorama.blue}LOGIN${colorama.reset}] ⇛ connected to discord via Discord.js@${discordVersion} | ${client.user.tag}`);
    client.user.setStatus("dnd");

    await registerCommands(client);
    await registerEvents(client);
});
client.login(process.env.token);
module.exports = {
    client,
    SchmandiClient
};