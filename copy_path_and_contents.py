import sublime
import sublime_plugin
import os

def get_plugin_settings():
	return sublime.load_settings("CopyPathAndContents.sublime-settings")


def get_separator():
	settings = get_plugin_settings()
	custom = settings.get("custom_separator", None)
	if isinstance(custom, str) and custom.strip() != "":
		return custom
	line_breaks = settings.get("line_breaks", 6)

	try:
		count = int(line_breaks)
		if count < 0:
			count = 0
	except (ValueError, TypeError):
		count = 6

	return os.linesep * count


def get_path_and_contents(view):
	file_path = view.file_name()
	if not file_path:
		return None

	try:
		with open(file_path, "r", encoding="utf-8") as f:
			file_contents = f.read()
		return f"{file_path}:{os.linesep}{file_contents}"
	except Exception as e:
		sublime.status_message(f"Failed to read {file_path}: {e}")
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
	def run(self, group=-1, index=-1):
		views = self._get_selected_views(group)

		entries = []
		for view in views:
			entry = get_path_and_contents(view)
			if entry:
				entries.append(entry)

		if entries:
			separator = get_separator()
			combined = separator.join(entries)
			sublime.set_clipboard(combined)
			sublime.status_message("Paths and contents of selected tabs copied to clipboard.")
		else:
			sublime.error_message("No valid files in selected tabs.")

	def is_enabled(self, group=-1, index=-1):
		return len(self._get_selected_views(group)) > 1

	def is_visible(self, group=-1, index=-1):
		return self.is_enabled(group, index)

	def _get_selected_views(self, group):
		selected_views = []
		for sheet in self.window.sheets():
			if sheet.group() == group and sheet.is_selected():
				view = sheet.view()
				if view and view.file_name():
					selected_views.append(view)
		return selected_views
