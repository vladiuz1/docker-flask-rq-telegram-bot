# flask, rq telegram bot

Its an overengineered template for running scheduled tasks with py, flask, rq, apscheduler...

If you know flask and rq, you will might it easy to deploy, otherwise just use cronjobs )

This app is doing the following:

- every few seconds it checks blockchain for QARK token movement (etherscan api), 
- notifies a channel of the movement.

was going to make a discord notifier too, but didn't bother with it.

To run it you will need docker.

very easy...

```
git clone git@github.com:vladiuz1/docker-flask-rq-telegram-bot.git
cd docker-flask-rq-telegram-bot
cp example.env .env
```

now edit the .env - and set your defaults.

you will need to create a telegram bot using @BotFather, create a group, invite two bots into
it: your newly created bot + @RawDataBot, so you can get your group_id.. don't forget to kick the bot
after you got the id.

you will need etherscan API key. Its free.


