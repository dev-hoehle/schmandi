const SchmandiClient = require("../../../index");
const { ChatInputCommandInteraction, InteractionResponse, SlashCommandBuilder } = require("discord.js");

module.exports = {
    name: "clone_emote",
    data: new SlashCommandBuilder()
        .setName('clone_emote')
        .setDescription('Clone an emote from another server to your server')
        .addStringOption(option =>
            option
                .setName('emoji')
                .setDescription('The emote you want to clone')
                .setRequired(true))
        .addStringOption(option =>
            option
                .setName('new_name')
                .setDescription('The name for the cloned emote')),
    
    /**
     * @param {ChatInputCommandInteraction} interaction
     * @param {SchmandiClient} client
     */
    async run(interaction, client) {
        try {
            const emojiStr = interaction.options.getString('emoji');
            const new_name = interaction.options.getString('new_name');

            // Check if the user has permission to manage emojis
            if (!interaction.member || !interaction.member.permissions.has('MANAGE_EMOJIS')) {
                const embed = {
                    title: "Permission Error",
                    description: `${interaction.user.toString()}, you don't have enough permissions to use this command.`,
                    color: 0xff0000,
                    footer: {
                        text: `Requested by ${interaction.user.username}`,
                        icon_url: interaction.user.displayAvatarURL({ format: 'png', dynamic: true })
                    }
                };
                return await interaction.reply({ embeds: [embed], ephemeral: true });
            }

            // Fetch the emoji object from the provided emoji string
            const emoji = client.emojis.cache.find(e => e.toString() === emojiStr);

            if (!emoji) {
                return await interaction.reply("Invalid emoji. Make sure to use a valid custom emoji.");
            }

            // Create the custom emoji
            const createdEmoji = await interaction.guild.emojis.create(emoji.url, new_name || emoji.name);

            const emojiEmbed = {
                title: 'Emote Cloned!',
                color: 0x00D9FF,
                description: `The emote \`${new_name || emoji.name}\` has been successfully cloned to this server!`,
                thumbnail: {
                    url: createdEmoji.url
                }
            };

            await interaction.reply({ embeds: [emojiEmbed] });
        } catch (error) {
            console.error(error);

            const errorEmbed = {
                title: 'Something went wrong',
                color: 0xff0000
            };

            await interaction.reply({ embeds: [errorEmbed], ephemeral: true });
        }
    },
};
