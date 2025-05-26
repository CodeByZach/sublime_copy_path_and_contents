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
	if not view:
		return None

	file_path = view.file_name()
	if not file_path or not os.path.isfile(file_path):
		return None

	try:
		with open(file_path, "r", encoding="utf-8") as f:
			file_contents = f.read()
		return f"{file_path}:{os.linesep}{file_contents}"
	except Exception as e:
		sublime.status_message(f"Failed to read {file_path}: {e}")
		return None


class CopyPathAndContentsCommand(sublime_plugin.WindowCommand):
	def run(self):
		sheet = self.window.active_sheet()
		view = sheet.view() if sheet else None

		if view and view.file_name():
			entry = get_path_and_contents(view)
			if entry:
				sublime.set_clipboard(entry)
				sublime.status_message("Path and contents copied to clipboard.")
				return

		sublime.error_message("No file path or contents available.")

	def is_enabled(self):
		sheet = self.window.active_sheet()
		return bool(sheet and sheet.view() and sheet.view().file_name())


class CopyPathsAndContentsOfSelectedTabsCommand(sublime_plugin.WindowCommand):
	def _get_selected_views(self):
		return [
			sheet.view()
			for sheet in self.window.sheets()
			if sheet.is_selected() and sheet.view() and sheet.view().file_name()
		]

	def run(self):
		views = self._get_selected_views()

		entries = []
		for view in views:
			entry = get_path_and_contents(view)
			if entry:
				entries.append(entry)

		if entries:
			sublime.set_clipboard(get_separator().join(entries))
			sublime.status_message("Paths and contents of selected tabs copied to clipboard.")
		else:
			sublime.error_message("No valid files in selected tabs.")

	def is_enabled(self):
		return len(self._get_selected_views()) >= 2

	def is_visible(self, hide_if_disabled=False):
		if hide_if_disabled:
			return self.is_enabled()
		return True
