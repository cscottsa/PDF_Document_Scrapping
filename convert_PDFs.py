# Author Christian Scott : 23 Jan 2023
# Initial script from:  https://github.com/daveshap/Document_Scraping

import os
import pdfplumber
from termcolor import colored

output_folder = 'converted/'

# function to save the text content of a pdf to a txt file
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

# function to print the final result of the conversion
def final_print(file_count, file_success_count, file_fail_count, file_failed_names):
    print('Files attempted: ' + str(file_count))
    print('Success: ' + str(file_success_count))
    print('Failed: ' + str(file_fail_count))
    if len(file_failed_names) != 0:
        for failed_file in file_failed_names:
            print(colored(failed_file, 'red'))
    print('#################################')

# function to convert pdf files in a directory to txt files
def convert_pdf2txt(src_dir, dest_dir):
    print('#################################\n# Starting .pdf to .txt conversion:')
    # create destination directory if it does not exist
    if not os.path.exists(dest_dir):
        print(colored('Not found', 'red') + ' output folder "' + colored(output_folder, 'red') + '"')
        os.makedirs(dest_dir)
        print(colored('Created', 'green') + ' output folder "' + colored(output_folder, 'green') + '"')
    # get list of pdf files in the source directory
    files = os.listdir(src_dir)
    files = [i for i in files if '.pdf' in i]
    file_count = 0
    file_success_count = 0
    file_fail_count = 0
    file_failed_names = []
    print('# Starting converstion')
    # iterate through pdf files
    for file in files:
        try:
            # open pdf
            with pdfplumber.open(src_dir+file) as pdf:
                file_count += 1
                output = ''
                i = 1
                # iterate through pages of pdf and extract text
                for page in pdf.pages:
                    output += page.extract_text()
                    output += '\n\nPAGE ' + str(i) + '\n\n'  # change this for your page demarcation
                    i += 1
                # save text to txt file
                save_file(dest_dir+file.replace('.pdf','.txt'), output.strip())
                file_success_count += 1
                print(colored(file, 'green') + ' successfully converted')
        except Exception as oops:
            file_count += 1
            file_fail_count += 1
            file_failed_names.append(file)
            print(colored(file, 'red') + ' failed to convert to .txt')
            print(oops, file)
    # print success rate after attempting all files
    final_print(file_count, file_success_count, file_fail_count, file_failed_names)
            
if __name__ == '__main__':
    convert_pdf2txt('PDFs/', output_folder)
