const SchmandiClient = require("../../../index");
const { ChatInputCommandInteraction, InteractionResponse, SlashCommandBuilder } = require("discord.js");

module.exports = {
    name: "userinfo",
    data: new SlashCommandBuilder()
        .setName("userinfo")
        .setDescription("Shows information about a user")
        .addUserOption(option =>
            option.setName("member")
                .setDescription("About which member do you want to get information?")),
                
    /**
     * @param {ChatInputCommandInteraction} interaction
     * @param {SchmandiClient} client
     */
    async run(interaction, client) {
        const member = interaction.options.getMember("member") || interaction.member;

        const userCreatedAt = member.user.createdAt.toLocaleString();
        const joinedAt = member.joinedAt.toLocaleString();

        const embed = {
            color: member.displayColor,
            thumbnail: {
                url: member.user.displayAvatarURL({ dynamic: true })
            },
            author: {
                name: `${member.displayName}'s Info`,
                icon_url: member.user.displayAvatarURL({ dynamic: true })
            },
            fields: [
                {
                    name: "Name",
                    value: `\`\`\`${member.user.username}\`\`\``,
                    inline: false
                },
                {
                    name: "Display Name",
                    value: `\`\`\`${member.displayName}\`\`\``,
                    inline: false
                },
                {
                    name: "ID",
                    value: `\`\`\`${member.id}\`\`\``,
                    inline: false
                },
                {
                    name: "Creation",
                    value: `\`\`\`${userCreatedAt}\`\`\``,
                    inline: false
                },
                {
                    name: "Avatar",
                    value: `[Click here](${member.user.displayAvatarURL({ dynamic: true })})`,
                    inline: false
                },
                {
                    name: "Joined",
                    value: `${joinedAt}`,
                    inline: true
                },
                {
                    name: "Nickname",
                    value: `${member.nickname || "None"}`,
                    inline: true
                },
                {
                    name: "Highest Role",
                    value: `${member.roles.highest.mention}`,
                    inline: true
                }
            ]
        };

        await interaction.reply({ embeds: [embed], ephemeral: false });
    }
};