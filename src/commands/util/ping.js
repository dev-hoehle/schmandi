const SchmandiClient = require("../../../index");
const { ChatInputCommandInteraction, InteractionResponse, SlashCommandBuilder } = require("discord.js");

module.exports = {
    name: 'ping',
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Replies with the ping'),

    /**
     * @param {ChatInputCommandInteraction} interaction
     * @param {SchmandiClient} client
     */
    async run(interaction, client) {
        const embedLoading = {
            color: 0x0033ff,
            author: {
                name: 'Checking Ping...',
                iconURL: 'https://anditv.dev/assets/images/bot/loading.gif'
            }
        };

        try {
            const sendLoading = await interaction.reply({
                embeds: [embedLoading],
                fetchReply: true
            });

            const pingMs = sendLoading.createdTimestamp - interaction.createdTimestamp;

            let color;
            if (pingMs <= 50) {
                color = 0x44FF44;
            } else if (pingMs <= 100) {
                color = 0xFFD000;
            } else if (pingMs <= 200) {
                color = 0xFF6600;
            } else {
                color = 0x990000;
            }

            const pingEmbed = {
                color: color,
                fields: [
                    {
                        name: 'Pong! in',
                        value: `${pingMs} ms`
                    }
                ]
            };

            await sendLoading.edit({ embeds: [pingEmbed] });
        } catch (error) {
            console.error(error);
        }
    }
};