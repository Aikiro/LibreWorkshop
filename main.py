import cmd, sys, subprocess, os, ast, urllib.request

class MyPrompt(cmd.Cmd):
	intro = "Welcome to LibreWorkshop. Type help or ? to list commands.\n"
	prompt = "> " 
	file = None

	def preloop(self):
		print("Preloop shit")
		SteamCmd.install()

	def do_test(self, arg):
		pass

	def do_list(self, arg):
		"Shows the mod list."
		modlist = ModList.read()
		if modlist:
			for mod in modlist:
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
		"Download mods from the mod list."
		SteamCmd.run("download", arg)

	def do_update(self, arg):
		"Update installed mods"
		SteamCmd.run("download", arg)


class ModList:
	filename = "modlist.txt"

	def create():
		with open(ModList.filename,"w") as file:
			return
	
	def exists():
		return os.path.isfile(ModList.filename)

	def not_empty():
		if ModList.exists():
			with open(ModList.filename,"r") as file:
				modlist = file.readline()
				if modlist:
					return True
		else:
			return False

	def read():
		if ModList.not_empty():
			with open(ModList.filename,"r") as file:
				modlist_read = file.readline()
			modlist = ast.literal_eval(modlist_read)
			return modlist
		else:
			return []

	def write(modlist):
		with open(ModList.filename, "w") as file:
			file.write(str(modlist))

	def add(mod):
		modlist = ModList.read()
		modlist.append(mod)

		ModList.write(modlist)

	def delete(mod):
		modlist = ModList.read()
		new_modlist = []
		for m in modlist:
		    if m[1] != mod:
		        new_modlist.append(m)
		
		ModList.write(modlist)

class SteamCmd:
	DOWNLOAD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
	path = "E:\\Programing\\SteamCMD\\steamcmd.exe"
	path_zip = "E:\\Programing\\LibreWorkshop\\steamcmd.zip"
	LOGIN = "+login anonymous"

	def installed():
		return os.path.isfile(SteamCmd.path_zip)

	def install():
		SteamCmd.download_steamcmd()

	def download_steamcmd():
		if not SteamCmd.installed():
			print("Requesting steamcmd.zip")
			steamcmd_zip = urllib.request.urlopen(SteamCmd.DOWNLOAD_URL)
			
			print("Downloading steamcmd.zip")
			steamcmd_zip = steamcmd_zip.read()
			
			print("Writing steamcmd.zip")
			with open('steamcmd.zip', 'wb') as fobj:
				fobj.write(steamcmd_zip)

			print("Downloading done.")


	def run(action, arg):
		if os.path.isfile(SteamCmd.path):
			function = getattr(SteamCmd, action)
			function()
		else:
			print("Error: SteamCmd not detected.")

	def download():
		modlist = ModList.read()
		if modlist:
			steamcmd_call = [SteamCmd.path, SteamCmd.LOGIN]
			for mod in modlist:
				steamcmd_call.append("+workshop_download_item {0} {1}".format(mod[0], mod[1]))
			steamcmd_call.append("+quit")
			
			subprocess.call(steamcmd_call)
			print("\nMods downloaded\n")

if __name__ == '__main__':
	MyPrompt().cmdloop()