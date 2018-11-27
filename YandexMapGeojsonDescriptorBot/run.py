import subprocess
import os

os.chdir(r'C:\Users\Bakhtiyar\source\repos\YandexMapGeojsonDescriptorBot\YandexMapGeojsonDescriptorBot')

os.putenv('HOME', '')

subprocess.call(['git', 'push', 'heroku', 'master'])

