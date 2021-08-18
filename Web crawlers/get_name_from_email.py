import csv

name_database = []
n = 0


def write_file(arg_data):
    with open('File_with_append_mail_and_Contact_Name.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(arg_data)


with open('File_with_append_mail_and_Contact_Name.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    header = ['Domain name', 'Company name', 'Phone', 'First name', 'Last Name', 'Email', 'Total reviews', 'Rating',
              'Provider certificate page link', 'Status', 'Vertical']
    writer.writerow(header)
with open('Names_DataBase.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        name_database.append(row[1].lower().strip())


def prepare_incoming_file():
    with open('File_with_append_mail.csv', 'r', encoding='UTF-8') as fwam:
        file_with_append_mail = csv.reader(fwam, delimiter=';')
        next(file_with_append_mail)
        for row_fwam in file_with_append_mail:
            cor_inc_row = []
            if len(row_fwam) != 0:
                cor_inc_row.append(row_fwam[0])
                cor_inc_row.append(row_fwam[1])
                cor_inc_row.append(row_fwam[2])
                cor_inc_row.append('')
                cor_inc_row.append('')
                cor_inc_row.append(row_fwam[3])
                cor_inc_row.append(row_fwam[4])
                cor_inc_row.append(row_fwam[5])
                cor_inc_row.append(row_fwam[6])
                cor_inc_row.append(row_fwam[7])
                cor_inc_row.append(row_fwam[8])
                correct_file.append(cor_inc_row)



def __main__(n):

    prepare_incoming_file()
    for r in correct_file:
    # with open('Correct_File.csv', 'r', encoding='utf-8') as f:
    #     reader = csv.reader(f, delimiter=';')
    #     next(f)


        # for r in reader:
            # print(r)
        data_row_with_name = r
            # -------- try find first name, second name, if in mail exist character "------

        if '@' in r[5]:
            item = r[5].split('@')[0].lower().strip()
            if '.' in item:
                first_item = item.split('.')[0]
                second_item = item.split('.')[1]
                if first_item in name_database and len(second_item) > 1:
                    n += 1
                    r[3] = first_item.capitalize()
                    r[4] = second_item.capitalize()
                elif first_item in name_database and len(second_item) <= 1:
                    r[3] = first_item.capitalize()
                    n += 1
                elif second_item in name_database and len(first_item) > 1:
                    n += 1
                    r[3] = second_item.capitalize()
                    r[4] = first_item.capitalize()
                    # print(data_row_with_name)
                elif second_item in name_database and len(first_item) <= 1:
                    n += 1
                    r[3] = second_item.capitalize()

            elif item in name_database:
                n += 1
                r[3] = item.capitalize()
                    # print(r[3])
            else:
                n += 1
                r[3] = 'Team'
                    # print('Team')
                # print(r[3])
        else:
            n += 1
        write_file(data_row_with_name)
        print("it is row number:", n)

correct_file = []
__main__(n)
