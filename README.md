<h1 align="center">schmandi</h1>
<p align="center">Just another discord.py Bot</p>


<details>
<summary>Setup</summary>
<ul>
   <li>Insert your Discord bot token from <a href="https://discord.com/developers/applications">Discord Developer Portal</a> in the file called <code>config.example.json</code> and rename it to <code>config.json</code>.</li>
   <li>Insert your <a href="https://developers.google.com/tenor/guides/quickstart">Tenor API key</a> in the <code>tenor_key</code> field of the <code>config.json</code> file. Otherwise the gifsearch command cannot be used.</li>
   <li>If you want the bot to greet new members, set the <code>greetmembers</code> field to <code>true</code> in the <code>config.json</code> file.<br>
   If you do not want the bot to greet new members, set the field to <code>false</code>.</li>
   <li>Run <code>pip install -r requirements.txt</code> to install the required packages.</li>
   <li>Run <code>python bot.py</code> to start the bot.</li>
</ul>
</details>

<details>
<summary>Admin commands</summary>
<ul>
  <li>ban: Bans a member from the server. 
    <ul>
      <li>member: The member you want to ban</li>
      <li>reason: Why do you want to ban this member?</li>
    </ul>
  </li>
  <li>kick: Kicks a member from the server.
    <ul>
      <li>member: The member you want to kick</li>
      <li>reason: Why do you want to kick this member?</li>
    </ul>
  </li>
  <li>lock_or_unlock: Locks or unlocks a channel.
    <ul>
      <li>channel: The channel you want to lock or unlock</li>
      <li>action: 'lock' or 'unlock'</li>
    </ul>
  </li>
 </ul>

</details>

<details>
<summary>Moderation commands</summary>
<ul>
  <li>nickname: Changes the bot's or a user's nickname
    <ul>
      <li>nickname: The nickname you want the bot or user to have</li>
      <li>member: The member whose nickname you want to change (optional)</li>
    </ul>
  </li>
  <li>clear: Deletes a certain number of messages
    <ul>
      <li>amount: The amount of messages to clear (1-100)</li>
    </ul>
  </li>
  <li>poll: Creates a simple poll
<ul>
<li>text: Your yes/no question</li>
</ul>

  </li>
  <li>say: Lets the bot say something (Use '\\\\' as linebrake)
    <ul>
      <li>message: The text you want the bot to say</li>
      <li>channel: The channel where the message will be sent (optional)</li>
    </ul>
  </li>
  </ul>
    <li>timeout: Timeout a Member
    <ul>
      <li>member: The member you want to timeout</li>
      <li>time: The time you want to mute the member</li>
    </ul>
  </li>
      <li>clone_emote: Clone an emote from another server to your server
    <ul>
      <li>emoji: The emote you want to clone</li>
      <li>new_name: The new name of the emoji</li>
    </ul>
  </li>
  </ul>


</details>

<details>
<summary>Util commands</summary>
<ul>
  <li>avatar: Shows the avatar of a user
    <ul>
      <li>member: The member whose avatar you want to view</li>
    </ul>
  </li>
  <li>base64decode: Decodes a Base64 string
    <ul>
      <li>text: What is your encoded text?</li>
    </ul>
  </li>
  <li>base64_encode: Base64 encodes a string
    <ul>
      <li>text: What is the text you want to encode?</li>
    </ul>
  </li>
  <li>yt: Direct-Download for your YT video
    <ul>
      <li>url: Which YT video do you want to download?</li>
    </ul>
  </li>
  <li>userinfo: Shows information about a user
    <ul>
      <li>member: About which member do you want to get infos?</li>
    </ul>
  </li>
</ul>
</details>


<details>
<summary>Fun commands</summary>
<ul>
  <li>roll: Rolls a virtual dice
    <ul>
      <li>sides: How many sides do you want?</li>
    </ul>
  </li>
  <li>gifsearch: Shows you a random gif for your query
    <ul>
      <li>query: Search query?</li>
    </ul>
  </li>
    <li>fact: Shows you a random and useless fact
    <ul>
      <li>language: the language in which you want to see the fact</li>
    </ul>
  </li>
</ul>
</details>
