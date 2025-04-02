## Requirements
`requirements.txt` is for docker services.
`requirements_screenshot.txt` is for the screenshot program.

## Chrome Driver
- [All version download](https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json)
- [Latest Version](https://googlechromelabs.github.io/chrome-for-testing/)

## QA
1. Error `selenium.common.exceptions.SessionNotCreatedException` occurs
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 122  
Current browser version is 128.0.6613.121 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe
```
Download the chrome driver corresponding to the version of chrome you are using. In this case, the version of chrome is 128.0.6613.121. Therefore, download the chromedriver from [this link](https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json) corresponding to this version. By searching "128.0.6613.121" 
