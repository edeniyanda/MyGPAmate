from appresources.update_table import update_table



data = update_table("mygpamatedata.db","100FirstSemester", "100", "Second")

file = data.load_course()


print(file)



