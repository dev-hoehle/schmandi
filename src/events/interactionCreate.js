const { EmbedBuilder, Events, Interaction, Message } = require("discord.js");
const { client } = require("../..");



const dcEvent = {
    name: Events.InteractionCreate,
    once: false,

    /**
     * @param {Interaction} interaction 
     * @returns {Promise<void>}
     */
    run: async function (interaction) {
        if (!interaction.isChatInputCommand()) return;
        if (!client) return;

        const commandCreate = client.commands.get(interaction.commandName);
        
        try {
            if (!commandCreate) {
                throw new Error("Invalid command");
            }
            
            await commandCreate?.run(interaction);
        } catch (err) {
            console.error(err);

            const invalidtextInput = new EmbedBuilder()
                .setColor("Red")
                .setAuthor(
                    {
                        name: "Something wrent wrong",
                        iconURL: "https://anditv.dev/assets/images/bot/error.png"
                    }
                )
                .setFooter(
                    {
                        text: `Requested by ${interaction?.user?.username}`,
                        iconURL: interaction?.user.avatarURL() ?? undefined
                    }
                )
            await interaction.reply(
                {
                    ephemeral: true,
                    embeds: [invalidtextInput]
                }
            )
        }
    }
};

module.exports = dcEvent;