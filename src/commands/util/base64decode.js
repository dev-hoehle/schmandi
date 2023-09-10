const SchmandiClient = require("../../../index");
const { ChatInputCommandInteraction, InteractionResponse, SlashCommandBuilder } = require("discord.js");
const base64 = require("base-64");

module.exports = {
    name: "base64_decode",
    data: new SlashCommandBuilder()
        .setName("base64_decode")
        .setDescription("Base64 decodes a string")
        .addStringOption(option =>
            option.setName("text")
                .setDescription("What is the text you want to decode?")
                .setRequired(true)),

    /**
     * @param {ChatInputCommandInteraction} interaction
     * @param {SchmandiClient} client
     */
    async run(interaction, client) {
        const text = interaction.options.getString("text");

        const stringBytes = Buffer.from(text, "utf-8");
        const base64String = base64.decode(stringBytes);

        const embed = {
            title: "Your decoded text:",
            description: `\`\`\`${base64String}\`\`\``,
            color: 0x00D9FF
        };

        await interaction.reply({ embeds: [embed], ephemeral: true });
    }
};