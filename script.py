import github
import os
import json
import jinja2

TEMPLATE_FILE = "template.html"

# ICONS
LOCATION = '&nbsp;<i class="fa fa-map-marker" aria-hidden="true"></i>&nbsp;'
COMPANY = '&nbsp;<i class="fa fa-building" aria-hidden="true"></i>&nbsp;'
BIO = '&nbsp;<i class="fa fa-user" aria-hidden="true"></i>&nbsp;'
GIT = '&nbsp;<i class="fa fa-github" aria-hidden="true"></i>&nbsp;'
PAPER = '&nbsp;<i class="fa fa-file-pdf-o" aria-hidden="true"></i>&nbsp;'
LINK = '&nbsp;<i class="fa fa-link" aria-hidden="true"></i>&nbsp;'


def _get_bio(user):
    # Create and return a biography for users
    return "".join([ "<br>" + COMPANY + user.company if user.company else "", "<br>" + LOCATION + user.location if user.location else "", "<br>" + BIO + user.bio if user.bio else ""])

def _git_data(id):
    # Find the github profile for a user
    git = github.Github(os.environ['GITHUBTOKEN'])
    user = git.get_user(id)
    return user
    
def load_template(template_file):
    # Load the template file as a jinja object
    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(TEMPLATE_FILE)
    return template

def build_profile(id, data):
    # Create profile pages based on the template
    temp = load_template(TEMPLATE_FILE)
    user = _git_data(id)
    output = temp.render(user=user.login, image=user.avatar_url,name=user.name, url=user.html_url, bio=_get_bio(user),data=data)

    with open(os.path.join(os.path.dirname(__file__), "participants", id + ".html"), "w") as profile:
        profile.write(output)
        print(output)

def main():
    with open("participants.json", "r") as file:
        data = json.load(file)

    for research in data.keys():
        for user in data[research]['participants']:
            profile = "".join(["participants/", user, ".html"])
            build_profile(user, data)
    
            

if __name__ == "__main__":
    main()