from datetime import datetime 


def sample_responses(input_text):


    user_message = str(input_text)

    if user_message in ("/chart","/chart@guardianfatherbot"):
        return "show me the chart"

    if user_message in ("/ca", "/contract", "/ca@guardianfatherbot", "/contract@guardianfatherbot"):
        return "show me the ca"

    if user_message in ("/buy", "/pancakeswap", "/buy@guardianfatherbot"):
        return "show me the pancakes link"






    