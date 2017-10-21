import cmd, sys, subprocess, os, ast, urllib.request, zipfile

class MyPrompt(cmd.Cmd):
	intro = "\nWelcome to LibreWorkshop. Type help or ? to list commands.\n"
	prompt = "> " 
	file = None

	def preloop(self):
		SteamCmd.install()

	def do_exit(self, arg):
		"Exits"
		exit()

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
		SteamCmd.run("download")

	def do_update(self, arg):
		"Update installed mods"
		SteamCmd.run("download")


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
	path_dir = "SteamCMD"
	path_exe = "SteamCMD\\steamcmd.exe"
	path_zip = "steamcmd.zip"
	LOGIN = "+login anonymous"

	def installed():
		return os.path.isfile(SteamCmd.path_exe)

	def install():
		if not SteamCmd.installed():
			print("\nLibreWorkshop needs SteamCMD to work, and it is not installed.")
			print("\nDo you want to download and install SteamCMD?")
			answer = input("> ")
			if (answer == "yes" or answer == "y" ):
				SteamCmd.download_steamcmd()
				SteamCmd.run("first_run")
			else:
				exit()

	def download_steamcmd():
		steamcmd_zip = urllib.request.urlopen(SteamCmd.DOWNLOAD_URL)
		steamcmd_zip = steamcmd_zip.read()
		with open(SteamCmd.path_zip, 'wb') as fobj:
			fobj.write(steamcmd_zip)

		SteamCmd.extract_steamcmd()

	def extract_steamcmd():
		if zipfile.is_zipfile(SteamCmd.path_zip):
			with zipfile.ZipFile(SteamCmd.path_zip) as zf:
				zf.extractall(path = SteamCmd.path_dir)

	def run(action):
		if os.path.isfile(SteamCmd.path_exe):
			function = getattr(SteamCmd, action)
			function()
		else:
			print("Error: SteamCmd not installed.")

	def first_run():
		subprocess.call([SteamCmd.path_exe, "+quit"])

	def download():
		modlist = ModList.read()
		if modlist:
			steamcmd_call = [SteamCmd.path_exe, SteamCmd.LOGIN]
			for mod in modlist:
				steamcmd_call.append("+workshop_download_item {0} {1}".format(mod[0], mod[1]))
			steamcmd_call.append("+quit")
			
			subprocess.call(steamcmd_call)
			print("\nMods downloaded\n")

if __name__ == '__main__':
	MyPrompt().cmdloop()