import cmd, sys, subprocess, os

class MyPrompt(cmd.Cmd):
	intro = "Welcome to LibreWorkshop. Type help or ? to list commands.\n"
	prompt = "> " 
	file = None

	mods = []
	steamcdm_path = "E:\\Programing\\SteamCMD\\steamcmd.exe"

	def do_hello(self, arg):
		"Says hello and your name"
		if arg:
			print("Hello {0}.".format(arg))
		else:
			print("Hello stranger.")

	def do_addmod(self, arg):
		"Adds a mod to the mod list. Type the Game ID and the ModID."
		self.mods.append(arg.split())

	def do_showmods(self, arg):
		"Shows the mod list."
		for mod in self.mods:
			print("Game ID: {0}, Mod ID: {1}".format(mod[0], mod[1]))

	def do_download(self, arg):
		"Launches SteamCMD and then quits."
		if os.path.isfile(self.steamcdm_path):
			subprocess.call([self.steamcdm_path, "+quit"])
			print("\nMods downloaded\n")
		else:
			print("Error: SteamCMD not detected at {0}".format(self.steamcdm_path))


if __name__ == '__main__':
	MyPrompt().cmdloop()