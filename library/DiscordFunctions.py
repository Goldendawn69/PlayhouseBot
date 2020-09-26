async def get_user_from_mention(mention):
    """
    Returns the ID when using <@####> mention in code where using the Member is required and not the user.

    Args:
        mention ([string]): The <@!#####> number that has been generated from user requests

    Returns:
        [int]: The Member/user number
    """
    if (mention.startswith('<@') & mention.endswith('>')):
        mention = mention[2:-1]

    if (mention.startswith('!')):
        mention = mention[1:]

    return int(mention)
