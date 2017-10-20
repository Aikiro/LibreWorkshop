import cmd, sys, subprocess, os

class MyPrompt(cmd.Cmd):
	intro = "Welcome to LibreWorkshop. Type help or ? to list commands.\n"
	prompt = "> " 
	file = None

	def do_list(self, arg):
		"Shows the mod list."
		modlist = ModList.read()
		if modlist:
			for line in modlist:
				mod = line.split()
				print("Game ID: {0}, Mod ID: {1}".format(mod[0], mod[1]))
		else:
			print("Modlist is empty.")

	def do_add(self, arg):
		"Adds a mod to the mod list. Type the Game ID and the ModID."
		ModList.add(arg.split())

	def do_delete(self, arg):
		"Deletes a mod from the Mod List. Type the the ModID."
		ModList.delete(arg)

	def do_download(self, arg):
		"Launches SteamCMD and then quits."
		SteamCmd.run("download", arg)

class ModList:
	filename = "modlist.txt"

	def create():
		if not ModList.exists():
			with open(ModList.filename,"w") as file:
				return
	
	def exists():

		return os.path.isfile(ModList.filename)

	def read():
		if ModList.exists():
			with open(ModList.filename,"r") as file:
				modlist = file.readlines()
			for line in modlist: line.rstrip()
			return modlist
		else:
			return None

	def add(mod):
		with open(ModList.filename, "a") as file:
			file.write("{0} {1}\n".format(mod[0], mod[1]))

	def delete(mod):
		read_modlist = ModList.read()
		with open(ModList.filename,'w') as write_modlist:
		    for line in read_modlist:
		        if line.split()[1] != mod:
		            write_modlist.write(line)

class SteamCmd:
	path = "E:\\Programing\\SteamCMD\\steamcmd.exe"
	login = "+login anonymous"

	def run(action, arg):
		if os.path.isfile(SteamCmd.path):
			function = getattr(SteamCmd, action)
			function()
		else:
			print("Error: SteamCmd not detected.")

	def download():
		modlist = ModList.read()
		if modlist:
			steamcmd_call = [SteamCmd.path, SteamCmd.login]
			modlist_to_line = ""
			for mod in modlist:
				steamcmd_call.append("+workshop_download_item " + mod.rstrip())
			steamcmd_call.append("+quit")
			
			print(steamcmd_call)
			subprocess.call(steamcmd_call)
			print("\nMods downloaded\n")

if __name__ == '__main__':
	MyPrompt().cmdloop()