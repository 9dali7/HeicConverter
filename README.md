# Heic Converter
A Simple Program For Windows That Converts Heic Images In PNG Format Built In Python

# Author
Dalibor Jovanovic

# My Setup Configuration
To make the executable and then the setup program I use pyinstaller and Inno setup.
I've made some aliases inside powershell to automate the setup.
To make it simple compile the main.py file with pyinstaller and rename the .exe file
with Heic Converter.exe and then run the setup-script.iss file with iscc (Inno Compiler)
to generate the Heic Converter-Setup.exe file

# My Powershell Profile Aliases
/**function inno-compile {
    param(
        [string]$path
    )

    if (-not $path) {
        Write-Host "Please provide the path to an Inno Setup script (.iss) file."
    }
    else {
        $innoPath = "C:\Program Files (x86)\Inno Setup 6\iscc.exe"
        $issFilePath = Resolve-Path $path  # Resolves relative path to absolute if needed
        & "$innoPath" "$issFilePath"
    }
/**}

/**Set-Alias iscc inno-compile


/**function compile-py {
    $AppName = Read-Host "Please Input The Program Name"

    pyinstaller --onefile --windowed --icon=icon.ico main.py

    Move-Item -Path .\dist\main.exe -Destination ".\$AppName.exe"

    iscc setup-script.iss

    Get-Process -Name main -ErrorAction SilentlyContinue | Stop-Process -Force

    Remove-Item -Force -Recurse .\build\ -ErrorAction SilentlyContinue

    Remove-Item -Force -Recurse .\dist\ -ErrorAction SilentlyContinue

    Remove-Item -Force -Recurse .\main.spec -ErrorAction SilentlyContinue

    Remove-Item -Force -Recurse ".\$AppName.exe" -ErrorAction SilentlyContinue
/**}

/**Set-Alias py-compile compile-py
