const SchmandiClient = require("../../../index");
const { ChatInputCommandInteraction, InteractionResponse, SlashCommandBuilder , contextMenuBuilder} = require("discord.js");
const axios = require('axios');
const { DateTime } = require('luxon');

module.exports = {
    name: "discord_status",
    data: new SlashCommandBuilder()
        .setName('discord_status')
        .setDescription('Shows you the Discord server status'),

    /**
     * @param {ChatInputCommandInteraction} interaction
     * @param {SchmandiClient} client
     */
    async run(interaction, client) {
        try {
            // Get the server status from the Discord status API using Axios
            const response = await axios.get('https://discordstatus.com/api/v2/summary.json');

            if (response.status !== 200) {
                throw new Error(`Unexpected HTTP status code: ${response.status}`);
            }

            const data = response.data;

            // Extract the component information from the API response
            const components = data.components.map((component) => ({
                name: component.name,
                value: component.status.charAt(0).toUpperCase() + component.status.slice(1),
                inline: true,
            }));

            // Create an embed to display the server status
            const embed = {
                title: data.status.description,
                description: `[Discord Status](https://discordstatus.com/)\n **Current Incident:**\n ${data.status.indicator}`,
                color: 0x00D9FF,
                timestamp: DateTime.now().toJSDate(),
                thumbnail: {
                    url: 'https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png',
                },
                fields: components,
            };

            await interaction.reply({ embeds: [embed] });
        } catch (error) {
            const errorEmbed = {
                title: 'Error while retrieving Discord status',
                description: error.message || 'An error occurred while fetching Discord status data.',
                color: 'DARK_RED',
            };
            await interaction.reply({ embeds: [errorEmbed] });
        }
    },
};

module.exports = {
    data: new SlashCommandBuilder()
        .setName('getmessageid')
        .setDescription('Get the ID of a message'),

    async execute(interaction) {
        const message = interaction.options.getMessage('message');
        await interaction.reply(`Message ID: ${message.id}`);
    },
};

// Create a context menu for "Get Message ID"
module.exports.contextMenu = {
    name: 'Get Message ID',
    type: 'MESSAGE',
    execute: async (interaction) => {
        await module.exports.execute(interaction);
    },
};