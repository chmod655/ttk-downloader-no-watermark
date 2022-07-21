import shutil

class Cleaner:

    def  __init__(self, dir, video_dir):
        self.dir = dir
        self.video_dir = video_dir

    def clean_cache(self):
        try: shutil.rmtree(self.dir)
        except: print('This cache was deleted!')

    def clean_cache_videos(self):
        try: shutil.rmtree(self.video_dir)
        except: print('This cache was deleted!')