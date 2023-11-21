import os
import click
import requests
import inquirer

def get_supported_languages():
    url = 'https://api.github.com/gitignore/templates'
    response = requests.get(url)

    if response.status_code == 200:
        templates = response.json()  # 直接使用 response.json()
        return templates
    else:
        return []

def generate_gitignore(language):
    url = f'https://raw.githubusercontent.com/github/gitignore/master/{language}.gitignore'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

@click.command()
def main():
    supported_languages = get_supported_languages()

    if not supported_languages:
        print('Failed to fetch supported languages. Please try again later.')
        return

    language_choices = supported_languages
    questions = [
        inquirer.List('language',
                      message='Select a programming language',
                      choices=language_choices),
    ]

    answers = inquirer.prompt(questions)

    language = answers['language']
    gitignore_content = generate_gitignore(language)

    if gitignore_content:
        with open('.gitignore', 'w') as gitignore_file:
            gitignore_file.write(gitignore_content)
        print(f'.gitignore file for {language} generated successfully.')
    else:
        print(f'Failed to generate .gitignore file for {language}. Please check if the language is valid.')

if __name__ == '__main__':
    main()
