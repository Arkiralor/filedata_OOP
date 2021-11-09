# File Discovery as per Last Modified Time

<p>
  A Python OOPs-based script to check a given directory for files and find all files that were modified after the script was last-accessed, then add the newly-modified file-names and file-data to a list of dictionaries and then push them to a remote system
</p>

The script consists of four (4) modules:

  1. Prototype.PY
 
    Contains the code to list out all recently modified files and send them to whatever requires it in JSON format.

  2. Ts_Init.PY
 
    Contains the code to initialize the timestamp file.

  3. Last_Access.TXT
 
    Contains the timestamp for when the script was last run.

  4. Time_Backup.TXT
 
    Contains a timestamp for before the files were created so it can be used to test the script; customise as per need.

## Operating Logic
1. A class object is created for the native class and the path to the directory containing the files <'path/to/files'> is provided as the argument.
2. The class then calls its 'main' method with the created object as the argument.
3. The script then checks for all files in the given directory and stores the names in the list.
4. The script then iterates through all the files (actually 'filenames' joined after the given 'path'.
  4.1. If the 'Last Modified Time' metadata of the file is after the timestamp in 'last-access.txt', the script parses through the file in 'binary' mode and encodes   the contents in 'base64' format.
  4.2. The name and contents of the file are added to a dictionary in {'file_name': <file name>, 'contents_base64': <encoded contents>}.
  4.3. The created dictionary is appended to a list of dictionaries.
5. The list of dictionaries is then returned to the calling function.
6. A login request is sent to the remote system and the file-transfer arguments are retrieved.
7. The file-transfer-arguments are used to send the list of dictionaries to the remote system in 'json' format.
