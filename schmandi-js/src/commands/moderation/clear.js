const SchmandiClient = require("../../../index");
const { ChatInputCommandInteraction, InteractionResponse, SlashCommandBuilder } = require("discord.js");

module.exports = {
    name: "clear",
    data: new SlashCommandBuilder()
        .setName('clear')
        .setDescription('Deletes a certain number of messages')
        .addIntegerOption(option =>
            option
                .setName('amount')
                .setDescription('The amount of messages to clear')
                .setRequired(true)
                .setMinValue(1)
                .setMaxValue(100)),

    /**
     * @param {ChatInputCommandInteraction} interaction
     * @param {SchmandiClient} client
     */
    async run(interaction, client) {
        try {
            // Check if the user has permission to manage channels
            if (!interaction.member.permissions.has('MANAGE_CHANNELS')) {
                return await interaction.reply({
                    content: `You don't have enough permissions to do that, ${interaction.user}.`,
                    ephemeral: true,
                });
            }

            const amount = interaction.options.getInteger('amount');
            const channel = interaction.channel;

            await interaction.reply({
                content: `Clearing ${amount} messages...`,
                ephemeral: true,
            });

            try {
                const messages = await channel.messages.fetch({ limit: amount });
                const deletedMessagesCount = messages.size;

                await channel.bulkDelete(messages);

                const successMessage = `**${deletedMessagesCount}** messages have been successfully deleted.`;
                const failureMessage = `Failed to delete **${amount - deletedMessagesCount}** of **${amount}** messages.`;

                const embed = {
                    title: "Messages Deleted",
                    color: 0x00EFDB,
                    description: `${successMessage}\n${failureMessage}`,
                    footer: {
                        text: `Requested by ${interaction.user.username}`,
                        icon_url: interaction.user.displayAvatarURL({ format: 'png', dynamic: true })
                    }
                };

                // Send the embed message in the channel
                return await interaction.followUp({ embeds: [embed] });
            } catch (error) {
                console.error(error);

                const errorResponse = 'An error occurred while deleting messages.';
                return await interaction.followUp(errorResponse);
            }
        } catch (error) {
            console.error(error);

            const errorResponse = 'An error occurred while processing the command. Please try again later.';
            return await interaction.reply({
                content: errorResponse,
                ephemeral: true,
            });
        }
    },
};