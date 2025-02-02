Set Shell zsh

Require pinkmess

Output docs/assets/gifs/quickstart/02-create-and-set-collection.gif

# Set up
Set FontSize 18
Set FontFamily "Comic Code Ligatures"
Set Margin 30
Set MarginFill "#e9618b"

# Commands
## Create a collection named "personal" in the directory ~/notes
Type "pinkmess collection create ~/notes --name personal"
Sleep 500ms
Enter
Sleep 2s

## Set the collection "personal" as the default collection
Type "pinkmess collection set personal"
Sleep 500ms
Enter
Sleep 3s