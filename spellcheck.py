import openai
import config


def gpt3(stext):
    openai.api_key = config.GPT_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=stext,
        temperature=0.1,
        max_tokens=3384,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    content = response.choices[0].text.split('.')
    return response.choices[0].text



with open('Text-Recognition/ex1.txt') as f:
    text = f.read()
query = f"The following text is from a scanned PDF document, correct all typos: {text}"
response = gpt3(query)
print(response)


querySpell = f"spell check this: {text} and return it as a string."
response = gpt3(querySpell)
print(response)
