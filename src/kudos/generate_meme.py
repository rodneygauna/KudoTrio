"""
Kudos - Meme Generator
This is a helper function to get a meme for a kudo.
"""

# Imports
import requests


# Function - Meme Templates
def meme_templates():
    """
    Using the memegen.link API, get a list of meme templates and
    return them as choices for the user to select from.
    """

    # Get list of meme templates
    response = requests.get("https://api.memegen.link/templates/")
    if response.status_code == 200:
        # Convert response to JSON
        response_json = response.json()
        # Create list of tuples for choices
        meme_choices = []
        for meme in response_json:
            meme_id = meme["id"]
            meme_name = meme["name"]
            meme_url = meme["_self"]
            meme_choices.append({
                "id": meme_id,
                "name": meme_name,
                "url": meme_url,
            })
        return meme_choices
    else:
        # Handle error if meme template list fails
        return []
