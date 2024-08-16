import random
import string
import json
import logging
import os

# Set up logging file
log_file = '0_data_generate.log'
if os.path.exists(log_file):
    os.remove(log_file)
# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def generate_keyword(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_DO_keyword_sets(num_sets, num_keywords_per_set):
    keyword_sets = {}
    for i in range(1, num_sets + 1):
        set_name = f"W^({i})"
        keyword_set = {f"w_{j}^({i})": generate_keyword(random.randint(5, 20)) for j in range(1, num_keywords_per_set + 1)}
        keyword_sets[set_name] = keyword_set
    return keyword_sets

def generate_DU_keyword_set(do_keyword_sets, num_keywords):
    all_keywords = [keyword for subset in do_keyword_sets.values() for keyword in subset.values()]
    selected_keywords = random.sample(all_keywords, num_keywords)
    keyword_set = {f"w_{i+1}": keyword for i, keyword in enumerate(selected_keywords)}
    return keyword_set

def save_keyword_sets(do_keyword_sets, du_keyword_set):
    with open('do_keyword_sets.json', 'w') as file:
        json.dump(do_keyword_sets, file, indent=4)
    info_string = f"Data owner keywords Set saved to file: {file.name}"
    logging.info(info_string)
    print(info_string)
    with open('du_keyword_set.json', 'w') as file:
        json.dump(du_keyword_set, file, indent=4)
    info_string = f"Data user keywords Set saved to file: {file.name}"
    logging.info(info_string)
    print(info_string)

def main():
    num_sets = 10
    num_keywords_per_set = 100
    num_du_keywords = 10

    logging.info(f"Data owner - Set Num: {num_sets}")
    logging.info(f"Keywords Per Set (Data owner): {num_keywords_per_set}")
    logging.info(f"Data owner: Search Keywords Number: {num_du_keywords}")

    do_keyword_sets = generate_DO_keyword_sets(num_sets, num_keywords_per_set)
    info_str = f"Data Owner Keywords: {num_sets*num_keywords_per_set} In Total - generated"
    logging.info(info_str)
    print(info_str)

    du_keyword_set = generate_DU_keyword_set(do_keyword_sets, num_du_keywords)
    info_str = f"Data User Keywords: {num_du_keywords} In Total - generated"
    logging.info(info_str)
    print(info_str)

    save_keyword_sets(do_keyword_sets, du_keyword_set)

if __name__ == '__main__':
    main()