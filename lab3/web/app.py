from flask import Flask
import cowsay
import quote


characters = ['beavis', 'cheese', 'cow', 'daemon', 'dragon', 'fox', 'ghostbusters', 'kitty',
'meow', 'milk', 'octopus', 'pig', 'stegosaurus', 'stimpy', 'trex', 
'turkey', 'turtle', 'tux']


def say_something(character, something):
    text = cowsay.get_output_string(character, something)
    text = text.replace('\n', '<br>')
    text = f"<pre>{text}</pre>"
    return text

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to python environemt tutorial."

@app.route('/<character>')
def animal(character):
    if character not in characters:
        return say_something('miki', "看屁喔")
    
    return say_something(character, quote.get_quote())

if __name__ == '__main__':
    app.run(debug=True)