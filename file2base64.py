import sys
from os import path
from base64 import b64encode, b64decode
import argparse
from glob import glob
from re import match


def file_encode(file_path:str, chunk_size:int=-1):
    '''
    convert any file to base64 encoded file(s)
    the splitted file has file extension as .64.xxx
    :param file_path: a valid file path
    :param chunk_size: by default -1, means does not split the file,
    if > 0, means split the file by given chunk size, measured in MB.
    NOTE: base64 encoded size could be larger than the original binary chunk size
    :return: None
    '''
    if path.exists(file_path):
        with open(file_path, 'rb') as rf:
            index = 0
            while raw:=rf.read(
                chunk_size * 1024 * 1024 if chunk_size > 0 \
                else -1
            ):
                index += 1
                encoded = b64encode(raw)
                output_path = path.join(
                    path.dirname(path.abspath(file_path)),
                    path.basename(file_path) + f'.64.{index:03d}'
                )
                with open(output_path, 'w') as wf:
                    wf.write(repr(encoded))
                print(f'=>{output_path}')
    else:
        print(f'File does not exist: {file_path}')


def file_decode(*file_paths):
    '''
    recover to original file from a list of .64.xxx files, the provided file list should belong to the same original file
    the recovered file has extension .r64
    :param file_paths: a list of .64.xxx file paths
    :return: None
    '''
    sorted_paths = sorted([file_path for file_path in file_paths if path.exists(file_path) \
                                                          and match('.*\.64\.\d+$', path.basename(file_path))
                           ])
    if sorted_paths:
        recovered_file_path = path.join(path.dirname(sorted_paths[0]),
                                           path.basename(sorted_paths[0]).rsplit('.64', maxsplit=1)[0] + '.r64'
                              )
        with open(recovered_file_path, 'wb') as wf:
            for file_path in sorted_paths:
                print(f'<={file_path}')
                with open(file_path, 'r') as rf:
                    raw = eval(rf.read())
                    decoded = b64decode(raw)
                    wf.write(decoded)
        print(f'=>{recovered_file_path}<=')
    else:
        print('No valid file provided')

def decode_by_file_name(file_name:str):
    file_list = glob(f'*{file_name}*.64.*')
    if file_list:
        file_decode(*file_list)
    else:
        print(f'Could not file matching files for {file_name}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', action='store_true', default=False, help='Indicate to convert file to base64 chunks of files')
    parser.add_argument('--merge', action='store_true', default=False, help='Indicate to convert base64 chunks of files back to original file')
    parser.add_argument('--file', action='store', required=True, help='File path for split or file name pattern for merge')
    parser.add_argument('--chunksize', action='store', default=-1,
                        help='Maximum size in MB to separate the original file into chunks, uses with --split. Be noted that chunks in base64 format could be larger than the raw bytes')

    args = parser.parse_args()
    if args.split and args.merge:
        print('--split and --merge can only pass one')
        sys.exit(1)
    if (not args.split) and (not args.merge):
        print('--split and --merge must specify one')
        sys.exit(2)

    if args.split:
        file_encode(args.file, chunk_size=int(args.chunksize))
    else:
        decode_by_file_name(args.file)