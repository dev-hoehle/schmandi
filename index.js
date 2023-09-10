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



class MentermaClient extends Client {
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

const client = new MentermaClient();



client.on("ready", async () => {
    if (!client?.user || !client || !client.application) {
        console.log("Somthin wrent wrong");
        process.exit(1);
    }

    console.log(`${sortTime()} [${colorama.green}INFO${colorama.reset}] [${colorama.blue}LOGIN${colorama.reset}] ⇛ Menterma | ${client.user.tag}`);
    client.user.setStatus("dnd");

    await registerCommands(client);
    await registerEvents(client);
});

client.login(process.env.token);
module.exports = {
    client,
    MentermaClient
};