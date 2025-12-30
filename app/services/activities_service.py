import storage

def store_activity(activity : dict):
    storage.activities.append(activity)

def get_all_activity():
    return storage.activities