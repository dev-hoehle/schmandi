const { EmbedBuilder } = require("discord.js");
const { MentermaClient } = require("../../index");
const { REST } = require("@discordjs/rest");
const { readdirSync } = require("fs");
const { join } = require("path");
const { green, reset, blue } = require("../lib/colorama");
const { sortTime } = require("../lib/util");
const { Routes } = require("discord-api-types/v9");


/**
 * @param {MentermaClient} botClient
 * @returns {Promise<void>}
 */

async function registerCommands(botClient) {
    if (!process.env.token || !process.env.application_id || !botClient) {
        console.log("Failed to get bot settings");
        process.exit(1);
    }

    const commands = [];
    const rest = new REST({ version: "10" }).setToken(process.env.token);

    const foldersPath = join(__dirname, "../commands");
    const commandFolders = readdirSync(foldersPath);
    
    for (const folder of commandFolders) {
        const commandsPath = join(foldersPath, folder);
        const commandFiles = readdirSync(commandsPath).filter(file => file);
        for (const file of commandFiles) {
            const filePath = join(commandsPath, file);
            const importCommand = require(filePath);

            if (!importCommand) {
                console.log(`Failed to sync ${filePath}`);
            } else if (importCommand?.data) {
                botClient?.commands?.set(importCommand.name, importCommand);

                commands.push(importCommand.data);
            } else {
                console.log(`Failed to sync ${filePath}`);
            }
        }
    }


    (async () => {
        try {
            await rest.put(
                Routes.applicationCommands(process.env.application_id.toString()),
                {
                    body: commands
                },
            );


            botClient.application?.commands.set(commands);

            botClient.commandsSynced = commands.length;
            console.log(`${sortTime()} [${green}INFO${reset}] [${blue}REGISTRY${reset}] ⇛ Registered ${commands.length} Commands`);
        } catch (error) {
            console.error(error);
        }
    })();
};

module.exports = registerCommands;