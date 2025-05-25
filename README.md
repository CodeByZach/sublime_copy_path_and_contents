# Copy Path and Contents
[![Latest Release](https://img.shields.io/github/tag/CodeByZach/sublime_copy_path_and_contents.svg?label=version)](https://github.com/CodeByZach/sublime_copy_path_and_contents/releases)

Copy Path and Contents is a Sublime Text plugin that allows you to quickly copy the full file path and contents of one or more open files to your clipboard. It's perfect for sharing code snippets with context or for backing up selected buffers in one go.

## Features

- 📄 Copy the current file’s path and contents.
- 🗂️ Copy all selected tabs’ paths and contents in the active group.
- ⚙️ Highly customizable output formatting:
  - Set a custom separator string between files.
  - Or define how many blank lines to use when separating each entry.

## Installation

Install via [Package Control](https://packagecontrol.io/installation):

1. Open the Command Palette: Ctrl+Shift+P / Cmd+Shift+P
2. Select: Package Control: Install Package
3. Search for: Copy Path and Contents

## Commands

| Command                                     | Description                                         |
|--------------------------------------------|-----------------------------------------------------|
| Copy Path and Contents                     | Copies the path and contents of the active file.    |
| Copy Paths and Contents of Selected Tabs   | Copies paths and contents of selected tabs (in group). |

Accessible via:
- Tools → Packages → Copy Path and Contents
- Tab context menu
- Command Palette

## Settings

You can customize the separator between file entries. Open settings via:

Preferences → Package Settings → Copy Path and Contents → Settings

Example:
```json
{
  // Number of blank lines used to separate file entries.
  // Only used when "custom_separator" is empty.
  "line_breaks": 6,

  // Optional string to use instead of blank lines (e.g., "---" or "====").
  // If set, this overrides "line_breaks".
  "custom_separator": ""
}
