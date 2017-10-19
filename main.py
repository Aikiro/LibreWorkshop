import cmd, sys, subprocess, os

class MyPrompt(cmd.Cmd):
	intro = "Welcome to LibreWorkshop. Type help or ? to list commands.\n"
	prompt = "> " 
	file = None

	steamcdm_path = "E:\\Programing\\SteamCMD\\steamcmd.exe"

	def do_add(self, arg):
		"Adds a mod to the mod list. Type the Game ID and the ModID."
		ModList.add(arg.split())

	def do_list(self, arg):
		"Shows the mod list."
		modlist = ModList.read()
		if modlist:
			for line in modlist:
				mod = line.split()
				print("Game ID: {0}, Mod ID: {1}".format(mod[0], mod[1]))
		else:
			print("Modlist is empty.")

	def do_download(self, arg):
		"Launches SteamCMD and then quits."
		if os.path.isfile(self.steamcdm_path):
			subprocess.call([self.steamcdm_path, "+quit"])
			print("\nMods downloaded\n")
		else:
			print("Error: SteamCMD not detected at {0}".format(self.steamcdm_path))

class ModList:
	filename = "modlist.txt"

	def create():
		if not ModList.exists():
			file = open(ModList.filename,"r")

	def exists():
		return os.path.isfile(ModList.filename)

	def read():
		if ModList.exists():
			file = open(ModList.filename,"r")
			return file.readlines()
		else:
			return None


	def add(mod):
		file = open(ModList.filename,"a")
		file.write("{0} {1}\n".format(mod[0], mod[1]))
		file.close()



if __name__ == '__main__':
	MyPrompt().cmdloop()