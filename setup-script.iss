#define MyAppName "HeicConverter"
#define MyAppExeName "HeicConverter.exe"
#define MyAppVersion "1.0"
#define MyAppPublisher "Dalibor Jovanovic"
#define MyAppIcon "icon.ico"
#define MyAppLicense "LICENSE"
#define MyReadMeFile "README.md"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
AppPublisher={#MyAppPublisher}
WizardStyle=modern
Compression=lzma2
SolidCompression=yes
OutputDir=.
OutputBaseFilename="{#MyAppName}-setup"
AppReadmeFile=README.md
LicenseFile={#MyAppLicense}

[Files]
Source: {#MyAppExeName}; DestDir: "{app}"
Source: {#MyReadMeFile}; DestDir: "{app}"; Flags: isreadme

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

