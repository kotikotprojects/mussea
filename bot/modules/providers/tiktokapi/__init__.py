from .content import TikTokPhotos, TikTokVideo
from .tiktok import TikTok

tiktokapi = TikTok()


__all__ = ["tiktokapi", "TikTokVideo", "TikTokPhotos"]
