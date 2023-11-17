"""
License
-------
    The MIT License (MIT)
    Copyright (c) 2017 Tashkel Project
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

@author: Github.com/Barqawiz
"""

from dotenv import dotenv_values

CFG = dotenv_values(".env")


class KEYS:
    # consumer_key
    TW_API_KEY = "thvWSVxTvsCvmHCa46G3KXVec"
    # consumer_secret
    TW_API_SEC = "e2mLYgVpoNPVBBF6gKAkDVjhI8vrXGg1FzSVHqwUnZTZ4EliZh"


# class CONNECT:
#     HOST = "0.0.0.0"
#     PORT = 8000
