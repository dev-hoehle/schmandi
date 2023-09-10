const fs = require("fs");
const path = require("path");
const { sortTime} = require("../lib/util");
const colorama = require("../lib/colorama");
const { MentermaClient } = require("../..");



/**
 * @param {MentermaClient} botClient
 * @returns {Promise<void>}
 */

async function registerEvents(botClient) {
    if (!process.env.token || !process.env.application_id || !botClient) {
        console.log("Failed to get bot settings");
        process.exit(1);
    }

    try {
        var eventsSynced = 0;
        const foldersPath = path.join(__dirname, "../events");
        const eventFolders = fs.readdirSync(foldersPath);
        

        for (const file of eventFolders) {
            eventsSynced++;
            const filePath = path.join(foldersPath, file);
            const importEvents = require(filePath);

            if (importEvents?.once) {
                botClient.once(importEvents?.name, (...args) => importEvents.run(...args));
            } else {
                botClient?.on(importEvents?.name, (...args) => importEvents.run(...args));
            }
        }

        botClient.eventsSynced = eventsSynced;
        
        console.log(`${sortTime()} [${colorama.green}INFO${colorama.reset}] [${colorama.blue}REGISTRY${colorama.reset}] ⇛ Registered ${eventsSynced} Events`);
    } catch (error) {
        console.error(error);
    }
};

module.exports = registerEvents;