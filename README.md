# street-movie
Google StreetView picture generate to movie, written in Python  
![optimized](https://github.com/hiroyuki-kasuga/street-movie/blob/master/misc/street_movie.gif?raw=true)

## Requirement
Python 2.7+  
MySQL 5+  
Pip 1.5+  
ffmpeg 2.4+   

example ffmpeg config

    ffmpeg version 2.4.4 Copyright (c) 2000-2014 the FFmpeg developers
      built on Dec 11 2014 10:26:44 with Apple LLVM version 6.0 (clang-600.0.56) (based on LLVM 3.5svn)
      configuration: --prefix=/usr/local/Cellar/ffmpeg/2.4.4 --enable-shared --enable-pthreads --enable-gpl --enable-version3 --enable-hardcoded-tables --enable-avresample --cc=clang --host-cflags= --host-ldflags= --enable-libx264 --enable-libmp3lame --enable-libxvid --enable-libtheora --enable-libvorbis --enable-libvpx --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-aacenc --enable-libfdk-aac --enable-libopenjpeg --disable-decoder=jpeg2000 --extra-cflags='-I/usr/local/Cellar/openjpeg/1.5.1_1/include/openjpeg-1.5 ' --enable-nonfree --enable-vda
      libavutil      54.  7.100 / 54.  7.100
      libavcodec     56.  1.100 / 56.  1.100
      libavformat    56.  4.101 / 56.  4.101
      libavdevice    56.  0.100 / 56.  0.100
      libavfilter     5.  1.100 /  5.  1.100
      libavresample   2.  1.  0 /  2.  1.  0
      libswscale      3.  0.100 /  3.  0.100
      libswresample   1.  1.100 /  1.  1.100
      libpostproc    53.  0.100 / 53.  0.100

## Install
clone this project

    git clone https://github.com/hiroyuki-kasuga/street-movie.git
    
install add module   

    pip install -r path/to/misc/pip
    
utf-8

    echo "import sys; sys.setdefaultencoding('utf-8')" > /path/to/site-packages/sitecustomize.py
    
change name settings_template.py and wsgi_template.py

    mv path/to/settings_template.py settings.py
    mv path/to/wsgi_template.py wsgi.py
    
change setting.py

    #change database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'street_movie',  # Or path to database file if using sqlite3.
            'USER': 'street_movie',  # Not used with sqlite3.
            'PASSWORD': 'changeme',  # Not used with sqlite3.
            'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
            'OPTIONS': {"init_command": "SET storage_engine=INNODB"},
            'ATOMIC_REQUEST': True,
        }
    }
    .......
    #change log file path
    LOGGING = {
        .....
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/path/to/app.log',
                'maxBytes': 1024 * 1024 * 5 * 100,  # 500MB
                'backupCount': 10,
                'formatter': 'standard'
            },
        .....
        },
        'loggers': {
        .....
        }
    }
    .....
    #change movie temporary destination path
    MOVIE_DEST_PATH = '/path/to/temporary/movie/directory'
    .....
    
    #change S3 access_key, secret_access_key and bucket_name
    AWS_ACCESS_KEY_ID = 'aws_access_key'
    AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'
    AWS_STORAGE_BUCKET_NAME = 'bucket_name'
    .....
    #change ffmpeg command path
    FFMPEG_COMMAND = '/path/to/ffmpeg -r 1 -i %s/%%05d.jpg -vcodec libx264 -qscale:v 0 %s'
    
DB migration

    cd path/to/src/main/street_movie/
    python ./manage.py syncdb
    
    
start server

    cd path/to/src/main/street_movie/
    python ./manage.py runserver

## Licence

[MIT](https://github.com/hiroyuki-kasuga/street-movie/blob/master/LICENSE)

## Author
[hiroyuki.kasuga](https://github.com/hiroyuki-kasuga)

