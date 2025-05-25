import sublime
import sublime_plugin

def get_path_and_contents(view):
	file_path = view.file_name()
	if not file_path:
		return None

	try:
		with open(file_path, "r", encoding="utf-8") as f:
			file_contents = f.read()
		return f"{file_path}:\n{file_contents}"
	except Exception as e:
		sublime.status_message(f"Failed to read {file_path}: {str(e)}")
		return None


class CopyPathAndContentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		entry = get_path_and_contents(self.view)
		if entry:
			sublime.set_clipboard(entry)
			sublime.status_message("Path and contents copied to clipboard.")
		else:
			sublime.error_message("No file path or contents available.")


class CopyPathsAndContentsOfSelectedTabsCommand(sublime_plugin.WindowCommand):
	def run(self, group, index):
		views = []

		for sheet in self.window.sheets():
			if sheet.group() == group and sheet.is_selected():
				view = sheet.view()
				if view and view.file_name():
					views.append(view)

		entries = []
		for view in views:
			entry = get_path_and_contents(view)
			if entry:
				entries.append(entry)

		if entries:
			combined = ("\n\n\n\n\n\n").join(entries)
			sublime.set_clipboard(combined)
			sublime.status_message("Paths and contents of selected tabs copied to clipboard.")
		else:
			sublime.error_message("No valid files in selected tabs.")
