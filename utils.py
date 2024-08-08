from pytube import YouTube

async def download_video(url, user_id):
      youtubeobject = YouTube(url)
      filesize = youtubeobject.streams.get_highest_resolution().filesize
      youtubeobject = youtubeobject.streams.get_highest_resolution()
    
      if (filesize // 1024 // 1024) <= 50:
      
            try:
                  filename = f"user_video_{user_id}"
                  youtubeobject.download(filename=filename)
                  return filename
            except:
                  return False
      else:
            return "50mb"