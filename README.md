<h1 align="center">schmandi</h1>
<p align="center">Just another discord.py Bot</p>


<details>
<summary>Setup</summary>
<ul>
   <br>
   Create a file called "config.json" with the following content:
   <br>
   <code>{"Token": ""}</code>
        <br>
   Insert your Token
     <br>
  Run pip install -r requirements.txt
  <br>
  Run python bot.py to start the bot.
</ul></details>

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
