## Email Notification Pusher Discord Bot

![medua-logos-cover-template](https://user-images.githubusercontent.com/113819648/196444896-934f4dfb-545c-41e3-a611-676486953ab6.jpg)

## About

### Participants

- `Omar Moustafa`:
    - `Twitter`: [@DevOmar100](https://twitter.com/devomar100)
    - `GitHub`: [@Omar8345](https://github.com/Omar8345)

### Description

A **Discord bot** powered by *Discord.py* connected with **Medusa.js** to serve your customers by keeping them ***up-to-date*** with the latest order updates!

### Preview

![image](https://user-images.githubusercontent.com/113819648/196449363-201fc17a-26a0-41a6-8d09-ab5a2a0a2ec5.png)


## Set up Project

### Prerequisites

Before starting the setup, please be sure to have the following ready-to-use:

- **Python3** installed on the machine
- **Medusa server** installed and accessible from the bot hosting machine

### Install Project

1. First of all, clone the GitHub repo:

```bash
$ git clone https://github.com/medusa-discord-email-notification-pusher medusa-discord-email
```

2. Change the directory and get your enviroment variables ready:

```bash
$ cd medusa-discord-email
$ mv .env.template .env
```

3. Open your `.env` file and add your keys, like the **SMTP server** and your **Discord bot token**.

4. After that you are ready to run your *Discord bot*, but you have to install any required **Python packages**:

```bash
$ pip install -r requirements.txt
```

5. Last but not least, you now get to run your bot:

```bash
$ python main.py
```

## Resources

- [**Medusa's** GitHub repository](https://github.com/medusajs/medusa)
- [**Python Downloads**](https://www.python.org/downloads/)