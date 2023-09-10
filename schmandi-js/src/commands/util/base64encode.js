const SchmandiClient = require("../../../index");
const { ChatInputCommandInteraction, InteractionResponse, SlashCommandBuilder } = require("discord.js");
const base64 = require("base-64");

module.exports = {
    name: "base64_encode",
    data: new SlashCommandBuilder()
        .setName("base64_encode")
        .setDescription("Base64 encodes a string")
        .addStringOption(option =>
            option.setName("text")
                .setDescription("What is the text you want to encode?")
                .setRequired(true)),

    /**
     * @param {ChatInputCommandInteraction} interaction
     * @param {SchmandiClient} client
     */
    async run(interaction, client) {
        const text = interaction.options.getString("text");

        const stringBytes = Buffer.from(text, "utf-8");
        const base64String = base64.encode(stringBytes);

        const embed = {
            title: "Your encoded text:",
            description: `\`\`\`${base64String}\`\`\``,
            color: 0x00D9FF
        };

        await interaction.reply({ embeds: [embed], ephemeral: true });
    }
};