import cgi

# Retrieve the user's question from the HTML form data
form = cgi.FieldStorage()
user_question = form.getvalue('question', '')

# Define the dictionary of predefined responses
responses = {
    'hello': 'Hello! How can I help you?',
    'how are you': 'I am doing well, thank you!',
    'goodbye': 'Goodbye! Have a nice day!',
    'default': 'Im sorry, but I dont understand your question.'
}

# Process the user's question and determine the appropriate response
response = responses.get(user_question.lower(), responses['default'])

# Print the response
print('Content-type: text/plain\n')
print(response)
