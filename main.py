import cmd, sys, subprocess, os, ast, urllib.request, zipfile, json

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
		ModList.create()

	def do_list(self, arg):
		"Shows the mod list."
		ModList.list()

	def do_add(self, arg):
		"Adds a mod to the mod list. Type the ModID."
		ModList.add(arg.split())

	def do_delete(self, arg):
		"Deletes a mod from the Mod List. Type the the ModID."
		ModList.delete(arg)

	def do_download(self, arg):
		"Download mods from the mod list."
		SteamCmd.run("download_mods")


class ModList:
	"This class controls the mod list. It has methods to add, delete, list, etc mods from the modist."
	"The mod list is a python list, with nested lists written in modlist.txt."
	"The structure is: [[GameId, ModId],[GameId, ModId],[etc, etc]]"
	
	filename = "modlist.json"

	def create():
		modlist = {"mods" : {}}
		with open(ModList.filename,"w") as file:
			json.dump(modlist, file)

	def list():
		modlist = ModList.read()
		for i, modid in enumerate(modlist["mods"], 1):
			print("[{i}] {title}".format(i = i, title = modlist["mods"][modid]["title"]))

	def exists():
		return os.path.isfile(ModList.filename)

	def read():
		if not ModList.exists(): ModList.create()
		
		with open(ModList.filename, "r") as file:
			modlist = json.load(file)
		return modlist

	def write(modlist):
		with open(ModList.filename,"w") as file:
			json.dump(modlist, file, sort_keys = True, indent = 4)
	
	def add(modsid):
		for modid in modsid:
			modjson = SteamWebApi.get_modjson(modid)
			moddata = JsonUtils.parse_modjson(modjson)

			modlist = ModList.read()
			
			modlist["mods"][modid] = {}
			modlist["mods"][modid]["title"] = moddata["mod_tittle"]
			modlist["mods"][modid]["gameid"] = moddata["gameid"]

			ModList.write(modlist)

	def delete(modid):
		modlist = ModList.read()
		del modlist["mods"][modid]
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
				SteamCmd.extract_steamcmd()
				SteamCmd.run("first_run")
			else:
				exit()

	def download_steamcmd():
		steamcmd_zip = urllib.request.urlopen(SteamCmd.DOWNLOAD_URL)
		steamcmd_zip = steamcmd_zip.read()
		with open(SteamCmd.path_zip, 'wb') as fobj:
			fobj.write(steamcmd_zip)

	def extract_steamcmd():
		if zipfile.is_zipfile(SteamCmd.path_zip):
			with zipfile.ZipFile(SteamCmd.path_zip) as zf:
				zf.extractall(path = SteamCmd.path_dir)

	def run(action):
		if not SteamCmd.installed():
			SteamCmd.install()
		
		function = getattr(SteamCmd, action)
		function()
			

	def first_run():
		"Runs steamcmd.exe for first time so it can auto-update."
		subprocess.call([SteamCmd.path_exe, "+quit"])

	def download_mods():
		steamcmd_call = [SteamCmd.path_exe, SteamCmd.LOGIN]
		modlist = ModList.read()

		for modid in modlist["mods"]:
			steamcmd_call.append("+workshop_download_item {} {}".format(modlist["mods"][modid]["gameid"], modid))
		
		steamcmd_call.append("+quit")
		subprocess.call(steamcmd_call)
		print("\nMods downloaded\n")

class SteamWebApi:
	STEAM_WEBAPI_KEY = "AAC8D1DCEBABCB787FBABC3FA27C2FBD"
	API_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
	DATA_VALUES = "key=AAC8D1DCEBABCB787FBABC3FA27C2FBD&itemcount=1&publishedfileids[0]="

	def get_modjson(modid):
		data = SteamWebApi.DATA_VALUES + modid
		encoded_data = data.encode('utf-8')

		modjson = urllib.request.urlopen(SteamWebApi.API_URL, data=encoded_data)
		modjson = modjson.read().decode('utf-8')

		return modjson

		"""print("writing json file")
		with open("modjson.txt", "w") as file:
			file.write(modjson)"""

class JsonUtils:
	def parse_modjson(modjson):   
		data = json.loads(modjson)
		
		mod_tittle = data["response"]["publishedfiledetails"][0]["title"]
		modid = data["response"]["publishedfiledetails"][0]["1163829480"]
		gameid = data["response"]["publishedfiledetails"][0]["consumer_app_id"]
		description = data["response"]["publishedfiledetails"][0]["description"]
		
		parsed_moddata = {"modid" : modid, "mod_tittle" : mod_tittle, "gameid" : gameid, "description" : description}

		return parsed_moddata



if __name__ == '__main__':
	MyPrompt().cmdloop()