const SchmandiClient = require("../../../index");
const { ChatInputCommandInteraction, InteractionResponse, SlashCommandBuilder } = require("discord.js");



module.exports = {
    name: "avatar",
    data: new SlashCommandBuilder()
        .setName("avatar")
        .setDescription("Displays the avatar of a user")
        .addUserOption(option =>
            option.setName("member")
                .setDescription("The member whose avatar you want to view")),

    /**
     * @param {ChatInputCommandInteraction} interaction
     * @param {SchmandiClient} client
     */
    async run(interaction, client) {
        const member = interaction.options.getMember("member") || interaction.member;

        const embed = {
            title: `Download ${member.displayName}'s Avatar`,
            url: member.user.displayAvatarURL({ format: 'png', dynamic: true }),
            color: 0x00EFDB,
            author: {
                name: `${member.displayName}'s Avatar`,
                url: `https://discord.com/users/${member.id}`,
                icon_url: member.user.displayAvatarURL({ format: 'png', dynamic: true })
            },
            image: {
                url: member.user.displayAvatarURL({ format: 'png', dynamic: true })
            },
            footer: {
                text: `Requested by ${interaction.user.username}`,
                icon_url: interaction.user.displayAvatarURL({ format: 'png', dynamic: true })
            }
        };

        await interaction.reply({ embeds: [embed] });
    }
};