Tool to split any file to textual base64 format files, and reverse back to original file

usage: file2base64.exe [-h] [--split] [--merge] --file FILE [--chunksize CHUNKSIZE] [--password PASSWORD]

options:
  -h, --help            show this help message and exit
  --split               Indicate to convert file to base64 chunks of files
  --merge               Indicate to convert base64 chunks of files back to original file
  --file FILE           File path for split or file name pattern for merge
  --chunksize CHUNKSIZE
                        Maximum size in MB to separate the original file into chunks, uses with --split. Be noted that chunks in base64 format could be larger than the raw bytes       
  --password PASSWORD   Enable encryption and decryption for --split and --merge respectively

