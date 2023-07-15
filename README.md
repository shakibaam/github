# Github System

This project aims to implement a system similar to Git, which is a distributed version control system. The system allows users to manage their files and repositories.

## Features

- Users can create repositories and have multiple repositories.
- Each repository is created on the server side upon user request.
- Users can create additional directories within their repositories.
- Users can commit and push their files to the repository with a commit message.
- Other users can pull files from the server repository.
- All files and directories in the repository need to be rewritten on the local side.

## Usage

To commit and push a file, use the following command:

commit&push -m "commit message" -f "./dir/file"
Replace `"commit message"` with your desired commit message and `"./dir/file"` with the path to the file you want to commit.
