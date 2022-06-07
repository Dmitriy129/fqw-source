import json
import os
import sys

from src.scripts import script1, script1Mock, script2, script2Mock

mainConfig = json.load(open('./configs/main.json'))
moodleRun1Configs = json.load(open('./configs/script1.json'))

print("os.environ", os.environ)

availableScripts = {
    "script1": lambda: script1(mainConfig, moodleRun1Configs),
    "script2": lambda: script2(mainConfig),
}

mockedScripts = {
    "script1": lambda mockNumber: script1Mock(mainConfig, moodleRun1Configs, mockNumber),
    "script2": lambda mockNumber: script2Mock(mainConfig, mockNumber),
}

print(sys.argv)
scriptName = None
isMock = None
mockNumber = None


if(len(sys.argv) >= 2):
    scriptName = sys.argv[1]
    if(len(sys.argv) >= 3):
        isMock = sys.argv[2] == "mock"
        if(len(sys.argv) >= 4):
            mockNumber = sys.argv[3]

selectedScript = None

if(isMock):
    if scriptName in mockedScripts:
        selectedScript = mockedScripts[scriptName]
        if(mockNumber != None and mockNumber.isdigit()):
            def selectedScript(): return mockedScripts[scriptName](
                int(mockNumber))

        else:
            print('Need mock grade number')
    else:
        print(f'Script "{scriptName}" not available')
else:
    if scriptName in availableScripts:
        selectedScript = availableScripts[scriptName]
    else:
        print(f'Script "{scriptName}" not available')

print(f'Script "{scriptName}" starting...')
selectedScript()
print("done")
