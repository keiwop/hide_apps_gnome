import os
import argparse

path_apps_list = "/_/src/python/hide_apps_list"
path_apps_list_sorted = "/_/src/python/hide_apps_list_sorted"
path_desktop_files = "/usr/share/applications"
#path_desktop_files = "/home/keiwop/.local/share/applications"

apps_already_hidden = []


def parse_list(path_list):
	apps_list = []
	print("\nPath to apps list: \"%s\""% path_list)

	with open(path_apps_list, "r") as file_apps_list:
		for app in file_apps_list:
			apps_list.append(app.strip("\n"))
	file_apps_list.close()
	return apps_list


def sort_list(apps_list):
	return list(sorted(set(apps_list)))


def sort_list_to_file(apps_list):
	apps_list = list(sorted(set(apps_list)))
	file_apps_list_sorted = open(path_apps_list_sorted, "w")
	for app in apps_list: 
		file_apps_list_sorted.write(app+"\n")
	file_apps_list_sorted.close()
	return apps_list


def test_app_exist(apps_list):
	apps_found = []
	apps_not_found = []
	for app in apps_list:
		app_file = path_desktop_files + "/" + app
		if os.path.isfile(app_file):
			apps_found.append(app)
		else:
			apps_not_found.append(app)

	if apps_not_found:
		print("\nApplications not found in the filesystem: ")
		for app in apps_not_found:
			print(app)
	
	return apps_found


def test_app_already_hidden(apps_list):
	global apps_already_hidden
	for app in apps_list:
		app_file = path_desktop_files + "/" + app
		with open(app_file, "r") as file_app:
			for line in file_app:
				if "NoDisplay=true" in line:
					apps_already_hidden.append(app)
		file_app.close()

	return sorted(list(set(apps_list) - set(apps_already_hidden)))


def hide_apps_list(path_apps_list):
	apps_list = parse_list(path_apps_list)
	apps_list = sort_list(apps_list)
	print("List: ", apps_list)

	apps_list = test_app_exist(apps_list)
	print("\nWorking on these files: \n", apps_list)

	apps_list = test_app_already_hidden(apps_list)
	print("\nApplications already hidden: \n", apps_already_hidden)
	print("\nApplications about to be hidden: \n", apps_list)
	
	print("")
	if apps_list != []:
		for app in apps_list:
			app_file = path_desktop_files + "/" + app
			try: 
				with open(app_file, "a") as file_app:
					file_app.write("NoDisplay=true\n")
				file_app.close()
				print(app, "is now hidden")
			except Exception:
				print("You need to launch the script with sudo to modify files in \"%s\""% path_desktop_files)	
	else:
		print("There are no applications to hide")


def hide_single_app(app):
	app_file = app
	try: 
		with open(app_file, "a") as file_app:
			file_app.write("NoDisplay=true\n")
		print(app, "is now hidden")
	except Exception:
		print("You need to launch the script with sudo to modify files in \"%s\""% path_desktop_files)	



def show_apps_list(path_apps_list):
	apps_list = parse_list(path_apps_list)
	apps_list = sort_list(apps_list)
	print("List: ", apps_list)

	apps_list = test_app_exist(apps_list)
	test_app_already_hidden(apps_list)
	
	apps_list = apps_already_hidden
	print("\nWorking on these files: \n", apps_list)

	print("")
	for app in apps_list:
		app_file = path_desktop_files + "/" + app
		with open(app_file, "r") as file_app:
			lines = file_app.readlines()
		file_app.close()
		try:
			with open(app_file, "w") as file_app:
				for line in lines:
					if line != "NoDisplay=true\n":
						file_app.write(line)
			file_app.close()
			print(app, "is now visible")
		except Exception:
			print("You need to launch the script with sudo to modify files in \"%s\""% path_desktop_files)	


def show_single_app(app):
	print("Showing", app)
	app_file = app
	with open(app, "r") as file_app:
		lines = file_app.readlines()
	file_app.close()
	try:
		with open(app_file, "w") as file_app:
			for line in lines:
				if line != "NoDisplay=true\n":
					file_app.write(line)
		file_app.close()
		print(app, "is now visible")
	except Exception:
		print("You need to launch the script with sudo to modify files in \"%s\""% path_desktop_files)	


def parse_arguments():	
	global path_apps_list
	global path_apps_list_sorted
	parser = argparse.ArgumentParser(description="Little python script to hide applications from being seen in the application overview. Without any arguments, the default is to hide apps.")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--hide", action="store_true", help="Hide programs contained in apps_list")
	group.add_argument("--show", "-s", action="store_true", help="Show programs contained in apps_list")
	parser.add_argument("apps", nargs="?", default=path_apps_list, help="The path of the apps to modify. Either file list or single .desktop file")
	parser.add_argument("--sort", nargs="?", default=path_apps_list_sorted, help="Sort your application list in file", metavar="file")
	args = parser.parse_args()

#	Default application list for hiding or showing
	apps = args.apps
	if apps == path_apps_list:
		print("Using default path for application list: ")
		print(apps)
		if args.hide or (not args.hide and not args.show):
			hide_apps_list(apps)
		else:
			show_apps_list(apps)
	else:
		file_name, file_extension = os.path.splitext(apps)
#		Hiding or showing is enabled for only one .desktop file
		if ".desktop" in file_extension:
			if path_desktop_files in apps: 
				apps = apps
			else:
				apps = path_desktop_files + "/" + apps
			if os.path.isfile(apps):
				print("Modifying a single file: ")
				print(apps)
				if args.hide or (not args.hide and not args.show):
					hide_single_app(apps)
				else:
					show_single_app(apps)
			else:
				print(apps, "is not recognized")		
#		Custom application list is used for hiding or showing apps	
		elif os.path.isfile(apps):
			print("Using custom path for application list: ")
			print(apps)
			path_apps_list = apps
			if args.hide or (not args.hide and not args.show):
				hide_apps_list(apps)
			else:
				show_apps_list(apps)
		else:
			print(apps, "is not recognized")
	
	
	if args.sort != path_apps_list_sorted:
		print("")
		if args.sort != None: 
			path_apps_list_sorted = args.sort

		sort_list_to_file(parse_list(path_apps_list))
		print("Path to apps list sorted: \"%s\""% path_apps_list_sorted)

parse_arguments()

