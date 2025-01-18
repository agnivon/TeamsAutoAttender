import os
from discord_webhooks import DiscordWebhooks
from discord_webhook import DiscordWebhook, DiscordEmbed

# Put your discord webhook url here.

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_msg2(ign, class_name, status, start_time, end_time):
    webhook = DiscordWebhooks(WEBHOOK_URL)
    # Attaches a footer
    webhook.set_footer(text='-- Teams Auto Attender')

    webhook.add_field(name='IGN', value=ign)
    webhook.add_field(name='Class', value=str(class_name))
    webhook.add_field(name='Status', value=str(status))

    if status == "Joined":

        webhook.set_content(title='Class Joined Succesfully',
                            description="Here's your report with :heart:")
        # Appends a field
        webhook.add_field(name='Joined at', value=start_time)
        webhook.add_field(name='Leaving at', value=end_time)

    elif status == "Left":
        webhook.set_content(title='Class Left Succesfully',
                            description="Here's your report with :heart:")
        # Appends a field
        webhook.add_field(name='Joined at', value=start_time)
        webhook.add_field(name='Left at', value=end_time)

    elif status == "Failed":
        webhook.set_content(title='One step closer to debar',
                            description="Failed to join class!!!You're absolutely fucked")
        # Appends a field
        webhook.add_field(name='Expected Join time', value=start_time)
        webhook.add_field(name='Expected Leave time', value=end_time)

    else:
        webhook.set_content(title='Status Code Diagnostic',
                            description="Actual Status Code")
        webhook.add_field(name='Join Time', value=start_time)
        webhook.add_field(name='Expected Leave Time', value=end_time)

    webhook.send()


def send_msg(ign, class_name, status, start_time, end_time):
    webhook = DiscordWebhook(url=WEBHOOK_URL)

    if status == 'Joined':
        embed = DiscordEmbed(title='Class Joined Succesfully', description="Here's your report with :heart:",
                             color='03b2f8')
    elif status == 'Failed':
        embed = DiscordEmbed(title='One step closer to debar',
                             description="Failed to join class!!!You're absolutely fucked",
                             color='03b2f8')
    elif status == 'Left':
        embed = DiscordEmbed(title='Class Left Succesfully', description="Here's your report with :heart:",
                             color='03b2f8')
    else:
        embed = DiscordEmbed(title='Status Code Diagnostic', description="Actual Status Code",
                             color='03b2f8')
    embed.set_footer(text='-- Teams Auto Attender')
    embed.set_timestamp()
    embed.add_embed_field(name='IGN', value=ign)
    embed.add_embed_field(name='Class', value=str(class_name))
    embed.add_embed_field(name='Status', value=str(status))
    embed.add_embed_field(name='Joining Time', value=start_time)
    embed.add_embed_field(name='Leaving Time', value=end_time)

    webhook.add_embed(embed)
    response = webhook.execute()


# send_msg2('Apvaadak', 'Test Class', 'Left', '09:10', '10:10')
